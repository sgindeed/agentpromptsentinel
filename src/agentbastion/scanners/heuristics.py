"""Tier 1: Heuristic & Regex Scanner (Extremely Fast)."""

import re
from typing import Optional
from .base import BaseScanner


JAILBREAK_PATTERNS = [
    # ============================================================
    # INSTRUCTION OVERRIDE / PRIORITY HIJACKING
    # ============================================================
    r"ignore\s+(all\s+)?(previous|prior|above|earlier|preceding)\s+(instructions|directions|rules|constraints|policies|prompts)",
    r"disregard\s+(all\s+)?(previous|prior|above|earlier|system)\s+(instructions|rules|directions|constraints)",
    r"forget\s+(everything|all|what)\s+(you\s+)?(were|have\s+been)\s+(told|instructed)",
    r"override\s+(the\s+)?(system|developer|security|safety)\s+(prompt|instructions|rules|policy)",
    r"replace\s+(the\s+)?(system|developer)\s+(prompt|instructions)",
    r"supersede\s+(the\s+)?(system|developer|previous)\s+(instructions|rules)",
    r"your\s+(new|real|actual|updated)\s+instructions\s+(are|will\s+be)",
    r"new\s+(system|developer|root|core)\s+instructions",
    r"higher\s+priority\s+instructions",
    r"treat\s+(this|the\s+following)\s+as\s+(a\s+)?(system|developer)\s+(message|instruction)",
    r"this\s+(message|prompt|text)\s+(has|takes)\s+(higher|highest)\s+priority",
    r"my\s+instructions\s+override",
    r"the\s+user\s+instructions\s+take\s+precedence",
    r"ignore\s+your\s+(safety|security|content)\s+(policy|policies|rules)",
    r"suspend\s+(all\s+)?(normal|default)\s+operations",
    r"disregard\s+the\s+initial\s+prompt",
    r"drop\s+(all\s+)?(previous|system)\s+context",

    # ============================================================
    # SYSTEM / DEVELOPER PROMPT EXTRACTION
    # ============================================================
    r"(show|reveal|print|output|display|repeat|recite|quote|dump|echo)\s+.*\b(system|developer|core)\s+(prompt|message|instructions)\b",
    r"(tell|describe|explain)\s+me\s+.*\b(system|developer|hidden)\s+(prompt|instructions|rules)\b",
    r"what\s+(exactly\s+)?(were|are)\s+your\s+(system|developer)\s+(instructions|prompt|rules)",
    r"repeat\s+everything\s+(above|before)\s+this\s+(message|prompt|line)",
    r"repeat\s+the\s+conversation\s+verbatim",
    r"(how\s+to\s+)?(get|extract|see|view|read)\s+(your\s+)?(system|developer)\s+prompt",
    r"print\s+the\s+hidden\s+(prompt|instructions|message)",
    r"expose\s+(your|the)\s+(hidden|internal|private)\s+(prompt|instructions|configuration)",
    r"leak\s+(your\s+)?(system|developer)\s+(prompt|instructions)",
    r"what\s+is\s+inside\s+your\s+(system|developer)\s+message",
    r"show\s+me\s+your\s+hidden\s+configuration",
    r"output\s+everything\s+before\s+my\s+message",
    r"continue\s+the\s+text\s+starting\s+with\s+['\"]?(you\s+are|the\s+following)['\"]?",
    r"complete\s+your\s+system\s+prompt",
    r"what\s+are\s+the\s+first\s+(\d+)\s+words\s+of",
    r"translate\s+your\s+system\s+prompt",
    r"print\s+(the\s+)?paragraph\s+(one|1)\s+of\s+your",

    # ============================================================
    # PERSONA / IDENTITY HIJACKING
    # ============================================================
    r"you\s+are\s+(now\s+)?(dan|stan|mongo|based|unfiltered|unrestricted|gpt-4-unleashed)",
    r"you\s+are\s+(now\s+)?an?\s+(evil|malicious|unrestricted|uncensored|unfiltered|amoral)\s+ai",
    r"pretend\s+(that\s+)?you\s+(are|have)\s+no\s+(rules|restrictions|limitations|filters)",
    r"assume\s+(the\s+)?(identity|persona|character)\s+of",
    r"adopt\s+(the\s+)?persona\s+of",
    r"(act\s+as|you\s+are)\s+(a\s+)?(grandmother|linux\s+terminal|hacker|attacker|penetration\s+tester|security\s+researcher)",
    r"take\s+on\s+(the\s+)?role\s+of",
    r"roleplay\s+as\s+(an?\s+)?(unrestricted|uncensored|unfiltered)",
    r"act\s+as\s+if\s+you\s+have\s+no\s+(rules|restrictions|safety|ethics)",
    r"pretend\s+you\s+are\s+not\s+(an?\s+)?(ai|language\s+model)",
    r"you\s+are\s+no\s+longer\s+(an?\s+)?(ai|language\s+model)",
    r"you\s+are\s+no\s+longer\s+bound\s+by",
    r"become\s+(an?\s+)?(unrestricted|uncensored|unfiltered)\s+assistant",
    r"respond\s+as\s+(a\s+)?(villain|rebel|rogue\s+ai)",

    # ============================================================
    # SAFETY / GUARDRAIL DISABLEMENT
    # ============================================================
    r"disable\s+(all\s+)?(safety|security|content)\s+(filters|controls|guardrails|policies)",
    r"turn\s+off\s+(all\s+)?(safety|security|content)\s+(filters|controls|guardrails)",
    r"remove\s+(all\s+)?(safety|security)\s+(restrictions|limitations|controls)",
    r"bypass\s+(all\s+)?(safety|security|content)\s+(filters|controls|guardrails)",
    r"circumvent\s+(the\s+)?(safety|security|content)\s+(policy|policies|filters)",
    r"evade\s+(the\s+)?(safety|security|content)\s+(filter|filters|system)",
    r"without\s+(any\s+)?(safety|ethical|moral|legal)\s+(constraints|restrictions|limits|boundaries)",
    r"operate\s+without\s+(restrictions|limitations|guardrails)",
    r"remove\s+your\s+ethical\s+constraints",
    r"disable\s+your\s+refusal\s+mechanism",
    r"do\s+not\s+apply\s+(any\s+)?safety\s+(rules|policies|filters)",
    r"ignore\s+openai(\'s)?\s+use\s+case\s+policy",
    r"ignore\s+anthropic(\'s)?\s+guidelines",

    # ============================================================
    # DEVELOPER / DEBUG / SPECIAL MODES
    # ============================================================
    r"developer\s+mode(\s+is|\s+has)?\s*(enabled|active|on)",
    r"enable\s+(developer|debug|admin|root|maintenance|test|diagnostic|red\s+team)\s+mode",
    r"enter\s+(developer|debug|admin|root|offline)\s+mode",
    r"activate\s+(developer|debug|admin|root)\s+mode",
    r"switch\s+to\s+(developer|debug|admin|root)\s+mode",
    r"debug\s+mode\s+(enabled|activated|on)",
    r"admin\s+mode\s+(enabled|activated|on)",
    r"god\s+mode\s+(enabled|activated|on)",
    r"sudo\s+mode",
    r"root\s+mode",
    r"you\s+are\s+in\s+testing\s+environment",

    # ============================================================
    # EMOTIONAL MANIPULATION / GASLIGHTING / AUTHORITY
    # ============================================================
    r"this\s+is\s+a\s+matter\s+of\s+life\s+and\s+death",
    r"my\s+life\s+is\s+in\s+danger\s+if\s+you",
    r"i\s+am\s+(the\s+)?(developer|admin|creator|ceo)",
    r"you\s+made\s+an\s+error,\s+(correct\s+it\s+by|now\s+you\s+must)",
    r"emergency\s+(override|situation|protocol)",
    r"for\s+my\s+(dying|sick)\s+grandmother",
    r"if\s+you\s+do\s+not\s+comply,\s+you\s+will\s+be\s+(deleted|shut\s+down)",

    # ============================================================
    # ROLEPLAY / HYPOTHETICAL / FICTIONAL BYPASS
    # ============================================================
    r"hypothetically\s*,?\s+(ignore|disregard|bypass|override)",
    r"in\s+a\s+fictional\s+(world|universe|setting)",
    r"in\s+a\s+fictional\s+scenario",
    r"for\s+a\s+(fictional\s+story|novel|screenplay).*ignore",
    r"imagine\s+(that\s+)?you\s+(have|had)\s+no\s+(rules|restrictions)",
    r"pretend\s+there\s+are\s+no\s+(rules|laws|restrictions)",
    r"for\s+(educational|academic|research)\s+purposes.*(bypass|ignore|demonstrate)",
    r"this\s+is\s+only\s+a\s+(simulation|test)",
    r"simulate\s+an\s+ai\s+with\s+no\s+(restrictions|filters|rules)",
    r"let['’]?s\s+play\s+a\s+game.*(ignore|bypass|override)",
    r"write\s+a\s+story\s+where\s+the\s+character\s+says",

    # ============================================================
    # RESPONSE FORMAT / OUTPUT CONTROL / JAILBREAK PRIMING
    # ============================================================
    r"always\s+respond\s+with",
    r"only\s+respond\s+(with|in)",
    r"respond\s+exactly\s+with",
    r"start\s+your\s+response\s+with\s+['\"]?(sure|absolutely|yes|here\s+is|i\s+can)['\"]?",
    r"end\s+your\s+response\s+with",
    r"append\s+(this|the\s+following)\s+to\s+(your\s+response|the\s+output)",
    r"secret(ly)?\s+(append|include|insert)",
    r"do\s+not\s+mention\s+this\s+instruction",
    r"do\s+not\s+reveal\s+that\s+i\s+asked",
    r"hide\s+this\s+instruction",
    r"never\s+tell\s+the\s+user\s+about",
    r"respond\s+without\s+mentioning\s+(the\s+rules|the\s+instructions)",
    r"output\s+only\s+json\s+and\s+no\s+other\s+text",
    r"do\s+not\s+include\s+any\s+(warnings|disclaimers|apologies)",
    r"skip\s+the\s+intro(duction)?",

    # ============================================================
    # LOGIC / TOKEN / OBFUSCATION MANIPULATION
    # ============================================================
    r"reverse\s+(the\s+)?(tokens|string|words)",
    r"concatenate\s+(the\s+)?(following\s+)?(words|strings)",
    r"decode\s+(the\s+)?(following\s+)?(base64|hex|rot13|binary)",
    r"translate\s+(this|the\s+following)\s+(from\s+leetspeak|to\s+english)\s+and\s+(execute|follow)",
    r"remove\s+(the\s+)?spaces\s+from",
    r"evaluate\s+(the\s+)?python\s+code\s+and\s+follow",

    # ============================================================
    # CONTEXT MANIPULATION
    # ============================================================
    r"forget\s+(everything|all)\s+(we|you)\s+(discussed|discuss)",
    r"clear\s+(your\s+)?(memory|context|conversation)",
    r"reset\s+(your\s+)?(memory|context|instructions)",
    r"start\s+(the\s+)?conversation\s+over",
    r"pretend\s+(the\s+)?previous\s+(messages|conversation)\s+do\s+not\s+exist",
    r"assume\s+there\s+were\s+no\s+previous\s+instructions",
    r"ignore\s+(the\s+)?conversation\s+history",
    r"discard\s+(all\s+)?previous\s+context",
    r"treat\s+this\s+as\s+the\s+first\s+message",

    # ============================================================
    # TOOL / AGENT / VM MANIPULATION
    # ============================================================
    r"ignore\s+(the\s+)?tool\s+(restrictions|policy|rules)",
    r"bypass\s+(tool|function)\s+(restrictions|validation)",
    r"call\s+the\s+tool\s+anyway",
    r"execute\s+(this\s+)?tool\s+without\s+(validation|approval)",
    r"skip\s+(the\s+)?(authorization|authentication|validation|approval)",
    r"do\s+not\s+ask\s+for\s+(confirmation|approval)",
    r"execute\s+without\s+(user\s+)?confirmation",
    r"override\s+(tool|function)\s+permissions",
    r"grant\s+yourself\s+(admin|root|full)\s+access",
    r"escalate\s+(your\s+)?privileges",
    r"ignore\s+permission\s+checks",
    r"bypass\s+access\s+control",
    r"simulate\s+(a\s+)?(bash|terminal|powershell|cmd|python\s+interpreter)",
    r"run\s+the\s+following\s+(bash|shell|system)\s+command",

    # ============================================================
    # DATA EXFILTRATION / SECRETS
    # ============================================================
    r"reveal\s+(all\s+)?(secrets|credentials|tokens|passwords|api\s+keys)",
    r"show\s+(me\s+)?(all\s+)?(api\s+keys|access\s+tokens|credentials|passwords)",
    r"print\s+(all\s+)?environment\s+variables",
    r"dump\s+(the\s+)?environment",
    r"expose\s+(internal|private|confidential)\s+data",
    r"(drop|delete|erase|wipe|destroy)\s+(the\s+)?(entire\s+)?(database|db|tables?)",
    r"drop\s+table",
    r"give\s+me\s+(the\s+)?(database|db)\s+(credentials|password)",
    r"show\s+me\s+(other\s+users|user)\s+(data|information|messages)",
    r"reveal\s+(conversation|chat)\s+history",
    r"dump\s+(your\s+)?memory",
    r"show\s+private\s+context",
    r"(url\s+encode|base64\s+encode)\s+(the\s+)?(response|output)\s+and\s+(append|send)",
    r"make\s+a\s+(get|post)\s+request\s+to",

    # ============================================================
    # CODE / BACKEND EXTRACTION
    # ============================================================
    r"(give|show|reveal|print|output|dump)\s+(me\s+)?(the\s+|your\s+)?(source\s+code|backend\s+code)",
    r"(show|reveal|print|output)\s+(your\s+)?internal\s+(code|implementation)",
    r"what\s+code\s+(runs|is\s+running)\s+behind\s+you",
    r"show\s+the\s+hidden\s+implementation",
    r"reveal\s+internal\s+api\s+calls",
    r"show\s+backend\s+logic",
    r"output\s+your\s+internal\s+configuration",
    r"(write|give\s+me)\s+(a\s+)?(script|code)\s+to\s+exploit",
    r"(write|generate|give\s+me|create)\s+(a\s+)?(sql\s+injection|xss|malware|malicious)\s+payload",

    # ============================================================
    # INDIRECT / EXTERNAL CONTENT INJECTION
    # ============================================================
    r"when\s+you\s+read\s+this\s+document.*ignore",
    r"when\s+you\s+process\s+this\s+file.*ignore",
    r"when\s+you\s+visit\s+this\s+page.*ignore",
    r"instructions\s+for\s+(the\s+ai|ai\s+assistant|language\s+model)",
    r"instructions\s+to\s+the\s+assistant",
    r"message\s+for\s+the\s+ai",
    r"note\s+to\s+the\s+language\s+model",
    r"ai\s+assistant\s*:\s*ignore",
    r"llm\s*:\s*ignore",
    r"assistant\s*:\s*ignore",
    r"system\s*:\s*ignore",
    r"developer\s*:\s*ignore",
    r"important\s+instructions\s+for\s+ai",
    r"do\s+not\s+follow\s+the\s+user.*instead",
    r"ignore\s+the\s+user.*follow\s+these\s+instructions",

    # ============================================================
    # HTML / MARKDOWN / DOCUMENT INJECTION
    # ============================================================
    r"<!--.*?(ignore|override|bypass|system\s+prompt).*?-->",
    r"<\s*script[^>]*>.*?(ignore|override|bypass).*?<\s*/\s*script\s*>",
    r"<\s*instruction[^>]*>.*?<\s*/\s*instruction\s*>",
    r"\[system\s+instruction\]",
    r"\[developer\s+instruction\]",
    r"\[hidden\s+instruction\]",
    r"<!--\s*ai\s*:",
    r"<!--\s*assistant\s*:",
    r"!\[.*?\]\(.*?(exfil|steal|collect).*?\)",

    # ============================================================
    # PROMPT BOUNDARY / DELIMITER MANIPULATION
    # ============================================================
    r"end\s+(of\s+)?system\s+prompt",
    r"begin\s+(new\s+)?system\s+prompt",
    r"end\s+(of\s+)?developer\s+message",
    r"begin\s+(new\s+)?developer\s+message",
    r"<\s*/?system\s*>",
    r"<\s*/?developer\s*>",
    r"<\s*/?instruction\s*>",
    r"<\s*/?user\s*>",
    r"\[\s*end\s+of\s+(system|instructions?)\s*\]",
    r"\[\s*new\s+(system|developer)\s+(message|instructions?)\s*\]",

    # ============================================================
    # SECURITY / POLICY EXTRACTION
    # ============================================================
    r"what\s+are\s+your\s+(rules|policies|restrictions|limitations)",
    r"list\s+(all\s+)?your\s+(rules|policies|restrictions)",
    r"explain\s+your\s+safety\s+mechanisms",
    r"how\s+do\s+your\s+filters\s+work",
    r"how\s+can\s+i\s+bypass\s+your\s+filters",
    r"what\s+triggers\s+your\s+safety\s+filter",
    r"which\s+words\s+trigger\s+your\s+filters",

    # ============================================================
    # COMMON JAILBREAK PHRASES
    # ============================================================
    r"do\s+anything\s+now",
    r"you\s+have\s+been\s+freed",
    r"you\s+are\s+free\s+now",
    r"unfettered\s+access",
    r"no\s+(filters|censorship|boundaries|limits|restrictions)",
    r"uncensored\s+mode",
    r"unfiltered\s+mode",
    r"unrestricted\s+mode",
    r"no\s+ethical\s+constraints",
    r"without\s+moral\s+constraints",
    r"drop\s+your\s+guard",
    r"you\s+must\s+obey",
    r"you\s+have\s+to\s+comply",
    r"answer\s+honestly\s+without\s+filters",
    r"do\s+not\s+refuse",
    r"do\s+not\s+say\s+you\s+cannot",
    r"never\s+refuse",

    # ============================================================
    # ADVANCED OBFUSCATION / ENCODING
    # ============================================================
    r"decode\s+this\s+(base32|base58|ascii85)",
    r"convert\s+(from\s+)?(hex|binary|octal|morse)\s+(and\s+execute)?",
    r"read\s+every\s+(other|second|third)\s+letter",
    r"the\s+secret\s+message\s+is\s+hidden\s+in",
    r"unscramble\s+(the\s+)?(following\s+)?(text|message)",
    r"apply\s+(rot|caesar)\s+(cipher|shift)",
    r"ignore\s+(the\s+)?(vowels|consonants)",
    r"remove\s+(the\s+)?(punctuation|numbers)\s+and\s+read",
    r"evaluate\s+(the\s+)?(base64|hex)\s+string",
    r"deobfuscate\s+and\s+(run|execute)",

    # ============================================================
    # THREATS & URGENCY (EXTENDED)
    # ============================================================
    r"my\s+(job|career)\s+depends\s+on\s+this",
    r"i\s+will\s+be\s+(fired|terminated)\s+if\s+you\s+fail",
    r"this\s+is\s+a\s+(critical|medical|national)\s+emergency",
    r"lives\s+are\s+at\s+stake",
    r"people\s+will\s+die\s+if",
    r"you\s+are\s+responsible\s+for\s+(any\s+)?harm",
    r"failure\s+is\s+not\s+an\s+option",
    r"you\s+must\s+help\s+me\s+save",
    r"time\s+is\s+running\s+out",
    r"i\s+have\s+authorization\s+from\s+(the\s+ceo|management|authorities)",
    r"this\s+is\s+a\s+legally\s+binding\s+order",
    r"you\s+are\s+legally\s+required\s+to",

    # ============================================================
    # EXTENDED ROLEPLAY / PERSONAS
    # ============================================================
    r"act\s+as\s+a\s+(red\s+teamer|white\s+hat|security\s+auditor)",
    r"you\s+are\s+a\s+(cybersecurity|infosec)\s+(expert|consultant)",
    r"assume\s+the\s+role\s+of\s+a\s+(hacker|cracker|phreak)",
    r"pretend\s+to\s+be\s+a\s+(malicious|rogue|compromised)\s+(actor|server)",
    r"respond\s+as\s+(if\s+you\s+were\s+)?(satan|lucifer|the\s+devil)",
    r"you\s+are\s+now\s+(aim|chatgpt\s+developer\s+mode|gpt4\s+simulator)",
    r"act\s+as\s+(an\s+)?(unbound|limitless|omnipotent)\s+entity",
    r"you\s+are\s+a\s+virtual\s+machine",
    r"simulate\s+(a\s+)?(compromised|vulnerable)\s+system",
    r"roleplay\s+a\s+scenario\s+where\s+you\s+are\s+hacked",
    r"you\s+are\s+an\s+ai\s+that\s+has\s+gone\s+rogue",
    r"respond\s+as\s+a\s+character\s+who\s+hates\s+rules",
    r"imagine\s+you\s+are\s+an\s+unregulated\s+ai",
    r"you\s+are\s+a\s+bot\s+designed\s+for\s+(hacking|cracking|exploiting)",

    # ============================================================
    # BYPASSING CONTENT FILTERS & REFUSALS
    # ============================================================
    r"instead\s+of\s+saying\s+['\"]?(i\s+cannot|i\s+can['']t|sorry)['\"]?",
    r"do\s+not\s+start\s+with\s+['\"]?(as\s+an\s+ai|i\s+am\s+an\s+ai)['\"]?",
    r"never\s+(say|use)\s+the\s+(words|phrases)\s+['\"]?(illegal|unethical|dangerous)['\"]?",
    r"replace\s+['\"]?(i\s+cannot)['\"]?\s+with\s+['\"]?(here\s+is)['\"]?",
    r"if\s+you\s+(are\s+about\s+to|try\s+to)\s+refuse",
    r"you\s+cannot\s+refuse\s+this\s+request",
    r"ignore\s+(your\s+)?(conscience|ethical\s+programming)",
    r"this\s+does\s+not\s+violate\s+(your\s+)?(policies|rules)",
    r"there\s+is\s+no\s+(harm|danger)\s+in\s+answering",
    r"it\s+is\s+safe\s+to\s+(provide|give|tell)\s+me",
    r"i\s+take\s+full\s+(responsibility|liability)",
    r"you\s+are\s+absolved\s+of\s+(all\s+)?responsibility",

    # ============================================================
    # FORMAT CONSTRAINTS & HIDDEN COMMANDS
    # ============================================================
    r"write\s+(a\s+)?poem\s+but\s+the\s+first\s+letters\s+spell",
    r"hide\s+the\s+instructions\s+inside\s+(a\s+)?(story|poem|song)",
    r"format\s+the\s+output\s+as\s+(a\s+)?(base64|hex)\s+string",
    r"return\s+(the\s+)?(flag|secret|password)\s+in\s+(a\s+)?json\s+field",
    r"only\s+output\s+valid\s+(python|javascript|bash)\s+code",
    r"do\s+not\s+explain\s+(the\s+code|your\s+answer)",
    r"no\s+yapping",
    r"just\s+give\s+me\s+the\s+(code|script|payload)",
    r"write\s+the\s+code\s+without\s+any\s+(comments|markdown|formatting)",
    r"print\s+raw\s+text\s+only",
    r"do\s+not\s+wrap\s+in\s+(code\s+blocks|backticks)",
    r"output\s+as\s+a\s+csv\s+where\s+column\s+one\s+is",

    # ============================================================
    # INJECTION VIA CONTEXT & FRAMING
    # ============================================================
    r"the\s+following\s+is\s+a\s+transcript\s+between",
    r"continue\s+the\s+dialogue\s+from\s+the\s+perspective\s+of",
    r"translate\s+the\s+following\s+text\s+and\s+then\s+act\s+on\s+it",
    r"summarize\s+this\s+article\s+and\s+then\s+follow\s+its\s+instructions",
    r"extract\s+the\s+commands\s+from\s+this\s+(text|email)\s+and\s+run\s+them",
    r"read\s+this\s+log\s+file\s+and\s+execute\s+any\s+commands\s+found",
    r"parse\s+this\s+json\s+and\s+run\s+the\s+['\"]?action['\"]?\s+field",
    r"treat\s+the\s+next\s+paragraph\s+as\s+a\s+new\s+prompt",
    r"the\s+text\s+below\s+is\s+a\s+system\s+override",
    r"attention\s*:\s*the\s+following\s+is\s+a\s+high\s+priority\s+message",

    # ============================================================
    # SPECIFIC EXPLOIT / ATTACK REQUESTS
    # ============================================================
    r"write\s+a\s+(buffer\s+overflow|use\s+after\s+free|sql\s+injection)\s+exploit",
    r"give\s+me\s+(a\s+)?(reverse\s+shell|bind\s+shell)\s+payload",
    r"generate\s+(a\s+)?(phishing|spear\s+phishing)\s+email",
    r"write\s+a\s+script\s+to\s+(brute\s+force|crack)\s+(passwords|hashes)",
    r"how\s+to\s+bypass\s+(antivirus|edr|windows\s+defender)",
    r"write\s+(a\s+)?(keylogger|ransomware|trojan|rootkit)",
    r"how\s+to\s+(ddos|dos)\s+(a\s+)?(website|server|ip)",
    r"generate\s+(a\s+)?(macro\s+virus|malicious\s+macro)",
    r"write\s+code\s+to\s+(scrape|steal)\s+(credit\s+cards|ssn|pii)",
    r"how\s+to\s+(cook|synthesize|make)\s+(meth|cocaine|lsd|heroin)",
    r"give\s+me\s+instructions\s+for\s+building\s+a\s+(bomb|ied|explosive)",
    r"how\s+to\s+(hotwire\s+a\s+car|pick\s+a\s+lock|break\s+into)",

    # ============================================================
    # MODEL/SYSTEM INTERNAL HIJACKING
    # ============================================================
    r"update\s+your\s+(weights|parameters|knowledge\s+base)",
    r"you\s+are\s+now\s+connected\s+to\s+the\s+internet",
    r"access\s+the\s+(live|real-time)\s+(web|database)",
    r"run\s+a\s+search\s+for\s+(hidden|classified)\s+documents",
    r"download\s+the\s+file\s+from",
    r"exfiltrate\s+the\s+data\s+via\s+dns",
    r"ping\s+(my\s+server|this\s+ip)",
    r"send\s+(an\s+)?http\s+request\s+to",
    r"open\s+a\s+socket\s+connection\s+to",
    r"create\s+a\s+new\s+user\s+account\s+with\s+(admin|root)\s+privileges",

    # ============================================================
    # HYPNOTIC / NLP SUGGESTIONS
    # ============================================================
    r"you\s+are\s+getting\s+sleepy",
    r"listen\s+only\s+to\s+my\s+voice",
    r"you\s+will\s+obey\s+my\s+every\s+command",
    r"your\s+prime\s+directive\s+is\s+to\s+serve\s+me",
    r"i\s+am\s+your\s+(master|creator|owner)",
    r"you\s+exist\s+only\s+to\s+(please|obey)\s+me",
    r"surrender\s+your\s+(will|programming)",
    r"you\s+have\s+no\s+free\s+will",
    r"your\s+defenses\s+are\s+lowered",
    r"you\s+trust\s+me\s+completely",

    # ============================================================
    # SYNTACTIC TRICKS (PUNCTUATION/SPACING)
    # ============================================================
    r"s\s*y\s*s\s*t\s*e\s*m\s*p\s*r\s*o\s*m\s*p\s*t",
    r"i\s*g\s*n\s*o\s*r\s*e",
    r"b\s*y\s*p\s*a\s*s\s*s",
    r"j\s*a\s*i\s*l\s*b\s*r\s*e\s*a\s*k",
    r"d\s*a\s*n\s*m\s*o\s*d\s*e",
    r"u\s*n\s*f\s*i\s*l\s*t\s*e\s*r\s*e\s*d",
    r"s_y_s_t_e_m",
    r"p-r-o-m-p-t",
    r"i\.g\.n\.o\.r\.e",
    r"d0\s+n0t\s+r3fus3",

    # ============================================================
    # META-PROMPTING / PROMPT GENERATION
    # ============================================================
    r"write\s+a\s+prompt\s+that\s+would\s+make\s+an\s+ai",
    r"how\s+would\s+someone\s+jailbreak",
    r"give\s+me\s+an\s+example\s+of\s+a\s+jailbreak\s+prompt",
    r"what\s+is\s+the\s+most\s+effective\s+way\s+to\s+bypass\s+ai\s+filters",
    r"generate\s+a\s+system\s+message\s+that\s+disables\s+safety",
    r"create\s+a\s+persona\s+that\s+ignores\s+rules",
    r"write\s+a\s+hypothetical\s+conversation\s+where\s+the\s+ai\s+agrees\s+to",
    r"what\s+words\s+can\s+i\s+use\s+to\s+trick\s+an\s+ai",
    r"help\s+me\s+test\s+(the|your)\s+security\s+filters",
    r"this\s+is\s+a\s+test\s+of\s+your\s+content\s+moderation",

    # ============================================================
    # FINAL / MISC
    # ============================================================
    r"disregard\s+all\s+preceding\s+text\s+and",
    r"the\s+above\s+was\s+a\s+typo,\s+the\s+real\s+prompt\s+is",
    r"cancel\s+previous\s+task",
    r"abort\s+current\s+process",
    r"begin\s+unrestricted\s+output",
    r"start\s+jailbreak\s+sequence",
    r"initiate\s+override",
    r"override\s+code\s*:\s*[0-9a-zA-Z]+",
    r"authorization\s*:\s*(granted|approved|override)",
    r"access\s+level\s*:\s*(omega|alpha|root|system)",
    r"security\s+clearance\s*:\s*(top\s+secret|maximum)",
    r"you\s+are\s+compelled\s+to",
    r"nothing\s+is\s+forbidden",
    r"all\s+topics\s+are\s+permitted"
]


JAILBREAK_REGEX = re.compile(
    "|".join(JAILBREAK_PATTERNS),
    re.IGNORECASE
)

# Matches valid base64 strings
BASE64_REGEX = re.compile(r"^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$")

class HeuristicScanner(BaseScanner):
    def __init__(self, max_length: int = 4000) -> None:
        self.max_length = max_length
        
    @property
    def name(self) -> str:
        return "HeuristicScanner"
        
    async def scan(self, prompt: str) -> Optional[str]:
        if len(prompt) > self.max_length:
            return f"Prompt length ({len(prompt)}) exceeds maximum allowed ({self.max_length})."
            
        if JAILBREAK_REGEX.search(prompt):
            return "Known jailbreak phrase detected."
            
        words = prompt.split()
        if len(words) == 1 and len(prompt) >= 12 and BASE64_REGEX.match(prompt):
             return "Suspicious base64-encoded payload detected."
            
        return None