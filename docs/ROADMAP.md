# Production-readiness roadmap

## P0 — correctness and safety

- [x] Fix the Send Message action so it schedules/sends rather than opening the log window.
- [x] Keep the Tkinter event loop responsive; do not run an infinite scheduler loop on the UI thread.
- [ ] Define one scheduling model and avoid scheduling the same recipient repeatedly on every UI interaction.
- [x] Validate international phone numbers, time values, empty messages, and personalization inputs before enqueueing.
- [x] Record outcomes accurately; an automation call is not proof of delivery or read status.
- [x] Show background worker errors on the UI thread safely.
- [x] Add confirmation before multi-recipient sends and a cancellation path.
- [ ] Require recipient opt-in and support suppression/opt-out lists before campaign features.

## P1 — reliability

**Implemented in this branch:** background scheduler loop, UI-safe result queue, recipient/message/time validation, contact-name personalization, duplicate in-memory schedule guard, and SQLite operation tests. The schedule is still in-memory and is lost on app exit; browser operations are not crash-safe.

- [ ] Add persistent scheduled jobs with timezone-aware timestamps and restart recovery.
- [ ] Add bounded retries with backoff and an error/dead-letter view.
- [x] Keep browser automation off the UI event loop; a persistent, explicitly serialized job queue remains future work.
- [ ] Add database transactions, context-managed connections, indexes, and duplicate-contact policy.
- [ ] Add database migration/versioning and backup/restore instructions.
- [ ] Redact phone numbers and message bodies from routine logs.
- [ ] Add graceful shutdown and safe cancellation.

## P2 — quality and release engineering

- [x] Add unit tests for validation, database operations, scheduling, and failure paths.
- [x] Add CI for supported Python versions, linting, and tests.
- [ ] Pin dependencies and automate dependency/security review.
- [ ] Test on intended desktop environments with a real WhatsApp test account.
- [ ] Document supported Python/browser combinations and known limitations.
- [ ] Add a clear license and versioned release process.

## Integration decision

For production business messaging, evaluate the official WhatsApp Business Platform. Browser-driven automation is fragile and may be incompatible with WhatsApp policies or interface changes. No code change alone can guarantee account safety or delivery without environment-specific tests.
