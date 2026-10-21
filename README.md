# Miomaci Fantasy Football 2026

A minimal public record of a September 9, 2026 fantasy-football draft with ten configured AI models and one organizer-built harness.

Of 150 selections, **96 were completed by the assigned AI and 54 by an organizer fallback**. The fallback selected in ascending player-ID order subject to roster legality. Its use ranged from zero picks for Gemini, Meta and xAI to fourteen for DeepSeek. The resulting teams reflect unequal amounts of organizer selection, so their scores cannot establish a clean ranking of model football skill.

Opening lineups were organizer-authored using the first feasible lineup in draft order, without a fresh injury check. The scored season treatment keeps those starters unchanged; AI management was inactive. Model-authored draft choices and organizer choices are recorded separately.

Opening lineups were recorded at 23:38:49 UTC on September 9, 2026, about 41 minutes before the first kickoff.

## Results and scope

- [Draft counts and observed model identities](data/draft_summary.json)
- [Player names, IDs and provenance for all 150 selections](data/draft_picks.json)
- [Player names and team rosters on miomaci.com](https://miomaci.com/fantasy-football/#rosters-title)
- [Exact team scores](data/team_scores.json): Week 1 recorded FINAL; Weeks 2–5 PROVISIONAL, using unchanged organizer-selected starters. Data review date: October 15, 2026. Week 6 and later are not included.
- [Source receipt metadata and fingerprints](data/source_receipts.json)
- [Historical commit anchors and original artifact fingerprints](PROVENANCE.json)

This first package contains derived summaries and a new offline verifier. It omits the original harness, raw provider answers, raw sports data, private records, databases and legacy Git history. Consequently it supports consistency and integrity checks of the included summaries, not independent replay of provider calls or complete recalculation from NFL statistics. Original code and additional evidence can be considered in later reviewed releases.

## Check the package

With Python 3.11 or newer, from this directory:

```text
python scripts/verify_release.py
python -m unittest discover -s tests
```

Neither command uses credentials, contacts a service, modifies the experiment or runs a draft. The verifier checks file hashes, the exact allowlist, all 150 pick numbers, the 96/54 split, team counts, common scoring weeks, integer totals and provisional ordering. Hashes establish content identity, not independent proof of the underlying events or prior public availability.

## Attribution and licenses

The design studied [FantasyFootballBench by Arya Tschand](https://github.com/aryatschand/FantasyFootballBench). This package includes no FantasyFootballBench code, prompts, datasets or private correspondence.

NFL source facts were collected using nflverse and Tank01, with research references obtained through Exa. Raw feeds and publisher content are omitted. See [data sources](DATA_SOURCES.md), [methods](METHODS.md), [omissions](OMITTED_FILES.md) and [license scope](LICENSE_SCOPE.md).

New verification code is MIT licensed. Project-authored documentation and derived records are offered under CC BY 4.0 only to the extent Jeremy Reichert holds the necessary rights. Those grants do not relicense third-party material or proprietary provider output.
