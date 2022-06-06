
import json

TEMP = {
    "id": "DG1",
    "title": "Flag Verification",
    "subtitle": "(For use by qualified individuals competing in online, point-based computer-hacking competitions.)",
    "notes": [
        "Submit recovered flag for points.",
        "Go to ctf.dicega.ng for instructions and the latest information."
    ],
    "sections": [
        {
            "num": "Part I",
            "title": "General Information",
            "type": "general",
            "fields": [
                {"type": "text", "num": 1, "name": "Name", "info": "as shown on your bash prompt"},
                {"type": "text", "num": 2, "name": "Team Name", "info": "must match registered team name on ctf.dicega.ng; disregard if not different from above"},
                {"type": "flag", "num": 3, "name": "Flag", "info": "must be valid"}
            ]
        },
        {
            "num": "Part II",
            "title": "Flag Verification",
            "type": "steps",
            "steps": [
                {
                    "num": "Step 1",
                    "title": "Initial Checks",
                    "lines": [
                        {"type": "choice", "num": 4, "msg": "Does line 3b consists entirely of characters mapping to ASCII codepoints 32 to 127 (inclusive)?"},
                        {"type": "op", "num": 5, "msg": "If you entered \"yes\" for question 4, enter 1. Otherwise, enter 0."},
                        {"type": "op", "num": 6, "msg": "Number of individual characters in 3b (disregarding entries 3a and 3c)."},
                        {"type": "op", "num": 7, "msg": "Multiply line 5 and line 6."},
                        {"type": "val", "num": 8, "val": 64},
                        {
                            "type": "choice",
                            "num": 9,
                            "msg": "Is line 7 equal to line 8?",
                            "yes": "Continue to Step 2.",
                            "no": "Stop. This flag is invalid."
                        }
                    ]
                },
                {
                    "num": "Step 2",
                    "title": "Splitting",
                    "lines": [
                        {"type": "op", "num": 10, "msg": "Enter the first half of line 3b."},
                        {"type": "op", "num": 11, "msg": "Enter the second half of line 3b."},
                        {"type": "op", "num": 12, "msg": "Enter the first half of line 10."},
                        {"type": "op", "num": 13, "msg": "Enter the second half of line 10."},
                        {"type": "op", "num": 14, "msg": "Enter the first half of line 11."},
                        {"type": "op", "num": 15, "msg": "Enter the second half of line 11."}
                    ]
                },
                {
                    "num": "Step 3",
                    "title": "Precheck",
                    "lines": [
                        {"type": "op", "num": 16, "msg": "Compute the sha256 hash of line 12 as a hex digest."},
                        {"type": "choice", "num": 17, "msg": "Is line 16 equal to c22645a78b8fb69322aa9ec64f9b07e5511bebd8607c1ca9329127eac125f69e?", "yes": "Continue to line 18.", "no": "Stop. This flag is invalid."},
                        {"type": "op", "num": 18, "msg": "Compute the sha256 hash of line 13 as a hex digest."},
                        {"type": "choice", "num": 19, "msg": "Is line 18 equal to 4b63c6049b1db271a050595ae6403a57be699ab4e4a285b36aa7e88dceea2ff9?", "yes": "Continue to line 20.", "no": "Stop. This flag is invalid."},
                        {"type": "op", "num": 20, "msg": "Compute the sha256 hash of line 14 as a hex digest."},
                        {"type": "choice", "num": 21, "msg": "Is line 20 equal to 443e74baf5711ac27461e7a363a877b32021902a22b37bb6558c1323c9c92b73?", "yes": "Continue to line 22.", "no": "Stop. This flag is invalid."},
                        {"type": "op", "num": 22, "msg": "Compute the sha256 hash of line 15 as a hex digest."},
                        {"type": "choice", "num": 23, "msg": "Is line 22 equal to b560939f06730bddaa649e1fb4cd241695dea937f7ff2331760a2a6a7ba977c1?", "yes": "Continue to Step 4.", "no": "Stop. This flag is invalid."}
                        
                    ]
                },
                {
                    "num": "Step 4",
                    "title": "Verification",
                    "lines": [
                        {"type": "op", "num": 24, "msg": "Complete \"Subflag XORification A\" (DG4-A) using line 12 as \"Field A\" (DG4-A, line 1). Enter the result (line 127) here."},
                        {"type": "op", "num": 25, "msg": "Complete \"Subflag Randification B\" (DG4-B) using line 13 as \"Field A\" (DG4-B, line 1). Enter the result (line 732) here."},
                        {"type": "op", "num": 26, "msg": "Complete \"Subflag Automatification C\" (DG4-C) using line 14 as \"Field A\" (DG4-C, line 1). Enter the result (line 72) here."},
                        {"type": "op", "num": 27, "msg": "Complete \"Subflag Virtualification D\" (DG4-D) using line 15 as \"Field A\" (DG4-D, line 1). Enter the result (line X) here."},
                        {"type": "op", "num": 28, "msg": "Add lines 24 through 27."},
                        {"type": "val", "num": 29, "val": 4},
                        {
                            "type": "choice",
                            "num": 30,
                            "msg": "Is line 29 equal to line 28?",
                            "yes": "Continue to Part III.",
                            "no": "Stop. This flag is invalid."
                        }
                    ]
                }
            ]
        },
        {
            "num": "Part III",
            "title": "Certification",
            "type": "certification"
        }
    ]
}

