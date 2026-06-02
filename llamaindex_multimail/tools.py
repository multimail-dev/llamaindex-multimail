"""LlamaIndex tool spec for the MultiMail API."""

from __future__ import annotations
from typing import List, Optional
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from multimail import MultiMail


class MultiMailToolSpec(BaseToolSpec):
    """LlamaIndex tool spec that wraps MultiMail API operations.

    Each public method becomes a tool that an agent can invoke.
    Initialize with your MultiMail API key to get started.
    """

    spec_functions = [
        "send_email",
        "check_inbox",
        "read_email",
        "reply_email",
        "search_contacts",
        "list_pending",
        "decide_email",
        "get_thread",
        "tag_email",
    ]

    def __init__(self, api_key: str, *, base_url: str = "https://api.multimail.dev"):
        self.client = MultiMail(api_key, base_url=base_url)

    def send_email(
        self,
        mailbox_id: str,
        to: List[str],
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        reply_to: Optional[str] = None,
    ) -> str:
        """Send an email from a MultiMail mailbox.

        The body is written in markdown. If the mailbox uses gated oversight,
        the email will be held for human approval before delivery.

        Args:
            mailbox_id: The mailbox ID to send from.
            to: Recipient email addresses.
            subject: Email subject line.
            body: Email body in markdown format.
            cc: CC addresses.
            bcc: BCC addresses.
            reply_to: Optional reply-to address.
        """
        result = self.client.send_email(
            mailbox_id, to=to, subject=subject, markdown=body, cc=cc, bcc=bcc
        )
        return f"Email queued -- id: {result['id']}, status: {result['status']}, thread: {result['thread_id']}"

    def check_inbox(
        self,
        mailbox_id: str,
        status: Optional[str] = None,
        limit: int = 20,
    ) -> str:
        """Check a mailbox for recent emails.

        Returns subject, sender, date, and status for each email.

        Args:
            mailbox_id: The mailbox ID to check.
            status: Filter by direction ('inbound' or 'outbound').
            limit: Number of emails to return (default 20).
        """
        result = self.client.list_emails(mailbox_id, limit=limit, direction=status)
        emails = result.get("emails", [])
        if not emails:
            return "Inbox is empty."
        lines = []
        for e in emails:
            lines.append(
                f"- [{e['direction']}] {e['subject']} -- from {e.get('from_address', '?')} ({e['status']})"
            )
            lines.append(f"  ID: {e['id']}")
        return "\n".join(lines)

    def read_email(self, mailbox_id: str, email_id: str) -> str:
        """Read the full content of a specific email.

        Returns subject, sender, recipients, date, status, and body text.

        Args:
            mailbox_id: The mailbox ID.
            email_id: The email ID to read.
        """
        e = self.client.get_email(mailbox_id, email_id)
        parts = [
            f"Subject: {e['subject']}",
            f"From: {e.get('from_address', '?')}",
            f"To: {', '.join(e.get('to_addresses', []))}",
            f"Date: {e.get('created_at', '?')}",
            f"Status: {e['status']}",
            f"Direction: {e['direction']}",
            "",
            e.get("text_body", "(no text body)"),
        ]
        if e.get("has_attachments"):
            parts.append(
                f"\nAttachments: {', '.join(a['name'] for a in e.get('attachments', []))}"
            )
        return "\n".join(parts)

    def reply_email(self, mailbox_id: str, email_id: str, body: str) -> str:
        """Reply to an existing email. Maintains the thread and preserves headers.

        Args:
            mailbox_id: The mailbox ID.
            email_id: The email ID to reply to.
            body: Reply body in markdown format.
        """
        result = self.client.reply_email(mailbox_id, email_id, markdown=body)
        return f"Reply queued -- id: {result['id']}, status: {result['status']}"

    def search_contacts(
        self, query: Optional[str] = None, mailbox: Optional[str] = None
    ) -> str:
        """Search the contact list by name or email address.

        Args:
            query: Search query string.
            mailbox: Optional mailbox filter (reserved for future use).
        """
        contacts = self.client.list_contacts(q=query)
        if not contacts:
            return "No contacts found."
        lines = [
            f"- {c.get('name', '(no name)')} <{c['email']}>" for c in contacts
        ]
        return "\n".join(lines)

    def list_pending(self, mailbox: Optional[str] = None) -> str:
        """List emails waiting for human approval.

        Use this to check what needs oversight review.

        Args:
            mailbox: Optional mailbox filter (reserved for future use).
        """
        pending = self.client.list_pending()
        if not pending:
            return "No emails pending approval."
        lines = []
        for e in pending:
            lines.append(
                f"- {e['subject']} -> {', '.join(e.get('to_addresses', []))}"
            )
            lines.append(f"  ID: {e['id']} | Status: {e['status']}")
        return "\n".join(lines)

    def decide_email(
        self,
        email_id: str,
        decision: str,
        reason: Optional[str] = None,
    ) -> str:
        """Approve or reject a pending email.

        Args:
            email_id: The email ID to approve or reject.
            decision: 'approve' or 'reject'.
            reason: Optional reason for the decision.
        """
        result = self.client.decide(email_id, decision, reason=reason)
        return f"Email {email_id} -- decision: {decision}, new status: {result.get('status', 'updated')}"

    def get_thread(self, mailbox_id: str, thread_id: str) -> str:
        """Get all emails in a conversation thread, ordered chronologically.

        Args:
            mailbox_id: The mailbox ID.
            thread_id: The thread ID.
        """
        result = self.client.get_thread(mailbox_id, thread_id)
        emails = result.get("emails", [])
        if not emails:
            return "Empty thread."
        lines = []
        for e in emails:
            lines.append(
                f"[{e['direction']}] {e.get('from_address', '?')}: {e['subject']}"
            )
            body = e.get("text_body", "")
            if body:
                preview = body[:200] + "..." if len(body) > 200 else body
                lines.append(f"  {preview}")
            lines.append("")
        return "\n".join(lines)

    def tag_email(
        self, mailbox_id: str, email_id: str, tags: List[str]
    ) -> str:
        """Add tags to an email for classification and retrieval.

        Tags are passed as a list of 'key=value' strings (e.g. ['category=support', 'priority=high']).

        Args:
            mailbox_id: The mailbox ID.
            email_id: The email ID to tag.
            tags: List of tags as 'key=value' strings.
        """
        tag_dict = {}
        for tag in tags:
            if "=" in tag:
                k, v = tag.split("=", 1)
                tag_dict[k] = v
            else:
                tag_dict[tag] = "true"
        self.client.set_tags(mailbox_id, email_id, tag_dict)
        return f"Tags set on {email_id}: {tag_dict}"
