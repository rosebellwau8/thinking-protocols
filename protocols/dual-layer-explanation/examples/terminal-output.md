# Example terminal output

Topic: fictional cache invalidation.

## Intuitive layer

A cache is a nearby copy. Invalidation removes or marks that copy when the original changes so readers do not keep seeing an old answer.

## Precise layer

The system associates cached data with freshness rules. Writes, version changes, or expiry signals make an entry ineligible for reads; coordination and delayed delivery determine how long stale reads remain possible.

## Alignment note

The nearby-copy analogy explains staleness but not distributed ordering, partial failure, or consistency guarantees.
