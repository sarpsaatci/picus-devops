# picus-devops

Assumed AWS user is configured with AWS CLI.
Takes pubKey from PICUS_PUBKEY environmental variable.
CustomerId is not used. Execute functionality could not be completed.

create: creates specified ec2 instance(Manager, Peer).

list-nodes: lists ec2 nodes with id, state and public IPs.

backup: takes a snapshot of specified instance.

list-backups: lists snapshots with their IDs.

rollback: rollbacks a volume with specified snapshot(ID).

list-all: lists ec2 nodes with id, state and public IPs.
