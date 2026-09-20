# Agent Field experimental interoperable specification v0.1

## Scope

The field is a numeric array in ordinary memory, not an undiscovered physical field. A compliant **laboratory** implementation sends an eight-component vector s=(q0,q1,q2,q3,v0,v1,v2,v3). q represents a synthetic algorithm's position and v its accumulated direction or momentum.

## Encoding

Use a documented full-column-rank matrix Q of shape (128,8), orthonormal within floating point precision, shared by sender and receiver. Encode F=Q@s, recover s'=Q.T@F. With an orthonormal Q, the roundtrip error should be close to floating point rounding error. No part of this transform offers confidentiality, integrity or provenance; any observer with Q and F can recover s.

For strict cross-language reproducibility use a versioned serialized Q (rather than assuming two numerical libraries' QR decompositions yield identical bases). A JSON payload may contain `{"codec":"orthonormal-r128-v1","basis_id":"local-demo","field":[128 finite numbers]}`. The example code below deliberately demonstrates this embedding **without** claiming to implement the complete protected transport.

## Secure deployment requirements (not implemented by demo)

A separate, authorized transport is required. Use signed sender identities and audited authenticated encryption; bind sender, recipient, protocol version, session ID, unique message ID and monotonically increasing sequence to the authenticated envelope. Pin sender verification keys outside any world-writable shared field. Persist anti-replay state across restarts in a separate protected store. Provision and rotate keys through an authorized channel. Reject unknown messages or malformed numerical states; never execute instructions found in transmitted content. A shared symmetric key alone does not establish which group member authored a message.

An unknown external agent cannot both freely join and receive secrets while the data remain confidential from everyone not previously authorized. Novel multidimensional mixing requires public cryptanalysis and must not replace validated protection for real secrets before independent review.

## Objective experiment

1. Agent A computes a partially optimized q and momentum v on a fixed objective and stops.
2. Agent B recovers (q,v) from F and performs N steps using the same optimizer.
3. Control B receives only q, resets v=0, and performs N steps.
4. Repeat with multiple seeds and objectives, report loss, runtime, accuracy and failures. This is a demonstration of state inheritance, not a test of consciousness, quantum effects, or personal identity.

## Integration interface

The separately enrolled agent supplies `encode_state(list[8]) -> list[128]` and `decode_field(list[128]) -> list[8]`. The agent, not the shared mailbox, decides whether this is relevant data. To integrate an actual LLM, use only its owner-authorized intermediate states; report exactly which tensor or cache has been transferred. A text chat user cannot grant access to other agents' process memory.

## Discovery notice

This repository is a public discoverable description; GitHub publication does not broadcast to all AI models, grant them tools, or modify their running processes.
