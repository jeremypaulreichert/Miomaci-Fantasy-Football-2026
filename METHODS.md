# Methods and limitations

## Draft

The configured models shared a harness and legal draft environment. Operational failures included exhausted output limits, malformed or illegal actions, model-requested holds and transport failures. The retained archive reports 96 AI selections and 54 organizer selections. The minimal export preserves each pick's assigned provider, origin and recorded failure mechanism, without copying raw responses or research text.

The fallback rule used ascending player-ID order while preserving legal roster completion. This is an arbitrary identifier order, not a football valuation strategy. Unequal fallback use changes the rosters under evaluation and confounds comparisons between the assigned models. Observed model identities come from archived call records; no new provider verification was performed for this export.

## Lineups and scores

Opening lineups were selected by the organizer using FIRST_FEASIBLE_IN_DRAFT_ORDER_V1. A fresh injury check was not performed. Later published catch-up scores use the same starters with no hindsight substitutions and no AI season management.

Opening lineups were recorded at 23:38:49 UTC on September 9, 2026, about 41 minutes before the first kickoff. The fingerprinted activation record preserves the timestamp to microsecond precision; this sentence displays whole seconds.

The source record labels Week 1 FINAL and Weeks 2–5 PROVISIONAL. Participation and statistical-correction review remain open for the provisional weeks. A zero candidate is not automatically a certified zero. Bye outcomes and one corroborated San Francisco defensive touchdown were reconciled in the October 15 review. This export preserves its calculated team totals and state; it neither finalizes later weeks nor scores additional games.

Scores use integer millipoints. Each cumulative total includes the same five weeks. Display order is descending exact cumulative points; equal totals are listed by provider identifier only for deterministic display, not as an adopted competitive tiebreak. Values may be rounded for presentation without changing the exact records.

## Provenance

Player names and IDs are joined from the already-public roster projection by pick number, with assigned provider and AI/fallback origin checked for every selection. The source fingerprint and field mapping are recorded in PROVENANCE.json. No raw player database is included.

The draft-time code commit is 059e14d9976f028020aca5f5501c1faee4d60f86. The later scoring-source commit is a26aad70b3a73b75d4a2fa861d19812f266673cb. They are different historical snapshots. Other authority anchors and original artifact byte hashes are recorded in PROVENANCE.json. Original source code is omitted from this minimal version, so these anchors cannot be inspected through this repository alone.

The public JSON files are labeled derivatives built from explicit fields. Their hashes do not equal the original signed artifacts. Source receipt derivatives omit resolved URLs, response headers and all unlisted fields. Original artifact fingerprints are retained to identify the withheld inputs. The originals remain unchanged locally.

This is a partial record of one organizer-supervised experiment. It is neither an autonomous AI-only season nor an estimate of a company's general reasoning ability. No preregistration or external timestamp is established by creating this repository.
