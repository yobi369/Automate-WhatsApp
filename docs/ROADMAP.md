# Production-readiness roadmap

## P0 — correctness and safety

- [x] Fix the Send Message action so it schedules/sends rather than opening the log window.
- [x] Keep the Tkinter event loop responsive; do not run an infinite scheduler loop on the UI thread.
- [x] Define recurring daily scheduling and prevent duplicate recipient/message/time schedules.
- [x] Validate international phone numbers, time values, empty messages, and personalization inputs before enqueueing.
- [x] Record outcomes accurately; an automation call is not proof of delivery or read status.
- [x] Show background worker errors on the UI thread safely.
- [x] Add confirmation before multi-recipient sends and a cancellation path.
- [ ] Require recipient opt-in and support suppression/opt-out lists before campaign features.

## P1 — reliability

**Implemented in this branch:** background scheduler loop, UI-safe result queue, recipient/message/time validation, contact-name personalization, duplicate-schedule protection, persistent SQLite schedule storage, startup restoration, schedule cancellation, and SQLite/validation tests. Browser operations are not crash-safe; a send already in progress may not be cancellable.

- [x] Persist recurring daily schedules in SQLite and restore them on startup. Timezone selection and crash-safe execution remain open.
- [ ] Add bounded retries with backoff and an error/dead-letter view.
- [x] Keep browser automation off the UI event loop. A durable, explicitly serialized execution queue and concurrency control remain future work.
- [ ] Standardize database transactions/context-managed connections across legacy functions and add a duplicate-contact policy.
- [ ] Add database migration/versioning and backup/restore instructions.
- [ ] Redact phone numbers and message bodies from routine logs.
- [ ] Add graceful shutdown and safe cancellation.

## P2 — quality and release engineering

- [x] Add unit tests for input validation and database contact/log/schedule operations. Scheduler timing and browser failure-path tests remain open.
- [x] Add CI for Python compilation and unit tests. Linting and a multi-version test matrix remain open.
- [ ] Pin dependencies and automate dependency/security review.
- [ ] Test on intended desktop environments with a real WhatsApp test account.
- [x] Document setup requirements and known limitations; a verified browser/platform compatibility matrix remains open.
- [ ] Add a clear license and versioned release process.

## Integration decision

For production business messaging, evaluate the official WhatsApp Business Platform. Browser-driven automation is fragile and may be incompatible with WhatsApp policies or interface changes. No code change alone can guarantee account safety or delivery without environment-specific tests.
