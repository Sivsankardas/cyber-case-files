"""
Content sources — fully pre-written, zero-cost (no AI API calls needed).

1. RSS_FEEDS -> fresh, real cyber news (pulled live, posted in English)
2. HISTORICAL_CASES -> pre-written bilingual (EN+HI) case dossiers, rotated forever
3. SECURITY_TIPS -> pre-written bilingual tips
"""

RSS_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://www.darkreading.com/rss.xml",
    "https://www.cisa.gov/cybersecurity-advisories/all.xml",
]

HISTORICAL_CASES = [
    {
        "title": "The Mirai Botnet",
        "year": 2016,
        "en": {
            "what": "A college student and friends built Mirai, malware that scanned the internet for IoT devices (routers, cameras, DVRs) still using factory-default passwords.",
            "method": "Mirai enslaved hundreds of thousands of devices into a botnet, then aimed their combined bandwidth at a single target.",
            "impact": "The botnet took down DNS provider Dyn, knocking Twitter, Netflix, Reddit, and PayPal offline across the US East Coast for hours.",
            "lesson": "Change every default password on every smart device you own. 'admin/admin' is still the #1 door hackers walk through.",
        },
        "hi": {
            "what": "एक कॉलेज छात्र और उसके दोस्तों ने Mirai मैलवेयर बनाया, जो इंटरनेट पर उन IoT डिवाइसेज़ (राउटर, कैमरा, DVR) को खोजता था जिनमें अभी भी फैक्ट्री डिफ़ॉल्ट पासवर्ड सेट थे।",
            "method": "Mirai ने लाखों डिवाइसेज़ को एक बॉटनेट में बदल दिया, फिर उनकी संयुक्त बैंडविड्थ को एक ही टारगेट पर केंद्रित कर दिया।",
            "impact": "इस बॉटनेट ने DNS प्रोवाइडर Dyn को ठप कर दिया, जिससे Twitter, Netflix, Reddit और PayPal जैसी सेवाएं अमेरिका के पूर्वी तट पर घंटों बंद रहीं।",
            "lesson": "अपने हर स्मार्ट डिवाइस का डिफ़ॉल्ट पासवर्ड बदलें। 'admin/admin' आज भी हैकर्स का सबसे पसंदीदा रास्ता है।",
        },
    },
    {
        "title": "WannaCry Ransomware Outbreak",
        "year": 2017,
        "en": {
            "what": "Ransomware built on a leaked NSA exploit called EternalBlue began spreading across the globe within hours, encrypting files on infected machines.",
            "method": "WannaCry exploited an unpatched Windows SMB vulnerability, letting it spread machine-to-machine without any user clicking anything.",
            "impact": "Over 200,000 computers in 150 countries were hit, including UK hospitals, forcing the NHS to cancel surgeries and divert ambulances.",
            "lesson": "Patch your systems. The fix for this exact vulnerability had been released months before the attack — unpatched systems paid the price.",
        },
        "hi": {
            "what": "NSA के लीक हुए एक्सप्लॉइट 'EternalBlue' पर आधारित रैंसमवेयर कुछ ही घंटों में दुनिया भर में फैलने लगा और संक्रमित मशीनों की फाइलें एन्क्रिप्ट करने लगा।",
            "method": "WannaCry ने Windows की एक अनपैच्ड SMB खामी का फायदा उठाया, जिससे यह बिना किसी यूज़र क्लिक के मशीन-दर-मशीन फैल गया।",
            "impact": "150 देशों में 2 लाख से ज़्यादा कंप्यूटर प्रभावित हुए, जिनमें ब्रिटेन के अस्पताल भी शामिल थे — सर्जरी रद्द करनी पड़ीं और एम्बुलेंस डायवर्ट करनी पड़ीं।",
            "lesson": "अपने सिस्टम को समय पर पैच करें। इस खामी का फिक्स हमले से महीनों पहले ही जारी हो चुका था — जिन्होंने पैच नहीं किया, उन्हें भारी कीमत चुकानी पड़ी।",
        },
    },
    {
        "title": "The Target Corporation Breach",
        "year": 2013,
        "en": {
            "what": "Attackers stole login credentials from a small HVAC vendor that had remote access to Target's network for billing purposes.",
            "method": "Using those stolen credentials, they pivoted into Target's internal network and installed malware on point-of-sale terminals nationwide.",
            "impact": "40 million credit and debit card numbers were stolen during the busiest shopping season of the year.",
            "lesson": "Your security is only as strong as your weakest third-party vendor. Always segment vendor access from core systems.",
        },
        "hi": {
            "what": "हमलावरों ने एक छोटी HVAC वेंडर कंपनी की लॉगिन जानकारी चुराई, जिसे बिलिंग के लिए Target के नेटवर्क तक रिमोट एक्सेस मिला हुआ था।",
            "method": "उसी चुराई हुई जानकारी का इस्तेमाल करके वे Target के आंतरिक नेटवर्क में घुसे और देशभर के पॉइंट-ऑफ-सेल टर्मिनलों में मैलवेयर इंस्टॉल कर दिया।",
            "impact": "साल के सबसे व्यस्त शॉपिंग सीज़न के दौरान 4 करोड़ क्रेडिट और डेबिट कार्ड नंबर चोरी हो गए।",
            "lesson": "आपकी सुरक्षा उतनी ही मज़बूत है जितनी आपकी सबसे कमज़ोर थर्ड-पार्टी वेंडर। वेंडर एक्सेस को हमेशा मुख्य सिस्टम से अलग रखें।",
        },
    },
    {
        "title": "Stuxnet",
        "year": 2010,
        "en": {
            "what": "A highly sophisticated worm, believed to be nation-state built, specifically targeted industrial control systems at Iran's Natanz nuclear facility.",
            "method": "Stuxnet exploited multiple zero-day vulnerabilities to physically speed up and destroy centrifuges, while feeding operators fake 'normal' readings.",
            "impact": "It's considered one of the first true cyberweapons — malware causing real-world physical destruction, not just data theft.",
            "lesson": "Critical infrastructure needs air-gapping and specialized security, not just standard IT defenses. The physical world is now a valid attack target.",
        },
        "hi": {
            "what": "एक अत्यंत उन्नत वर्म, जिसे किसी देश-प्रायोजित समूह द्वारा बनाया गया माना जाता है, ने खासतौर पर ईरान के नतांज़ परमाणु संयंत्र के औद्योगिक नियंत्रण सिस्टम को निशाना बनाया।",
            "method": "Stuxnet ने कई ज़ीरो-डे खामियों का फायदा उठाकर सेंट्रीफ्यूज को तेज़ी से घुमाकर नष्ट कर दिया, जबकि ऑपरेटरों को स्क्रीन पर सब कुछ 'सामान्य' दिखाया जाता रहा।",
            "impact": "इसे पहले सच्चे साइबर-हथियारों में से एक माना जाता है — ऐसा मैलवेयर जिसने सिर्फ डेटा चोरी नहीं बल्कि वास्तविक भौतिक विनाश किया।",
            "lesson": "महत्वपूर्ण इंफ्रास्ट्रक्चर को सिर्फ सामान्य IT सुरक्षा नहीं, बल्कि एयर-गैपिंग और विशेष सुरक्षा उपायों की ज़रूरत है। अब भौतिक दुनिया भी एक वैध हमले का लक्ष्य है।",
        },
    },
    {
        "title": "The Twitter Bitcoin Scam Hack",
        "year": 2020,
        "en": {
            "what": "A 17-year-old social-engineered Twitter employees over the phone, convincing them to hand over access to internal admin tools.",
            "method": "With that access, the attacker hijacked verified accounts of Obama, Musk, Apple, and others to post a 'send Bitcoin, get double back' scam.",
            "impact": "The scam netted over $100,000 in Bitcoin within hours, and exposed how a single social-engineering call could compromise a major platform.",
            "lesson": "The weakest link in security is often a human on the phone, not a firewall. Train staff to verify identity before granting any access.",
        },
        "hi": {
            "what": "17 साल के एक लड़के ने फोन पर Twitter के कर्मचारियों को सोशल इंजीनियरिंग के ज़रिए बहलाकर आंतरिक एडमिन टूल्स तक पहुंच हासिल कर ली।",
            "method": "उस एक्सेस का इस्तेमाल करके हमलावर ने ओबामा, मस्क, एप्पल जैसे वेरिफाइड अकाउंट्स को हैक कर 'बिटकॉइन भेजो, डबल पाओ' वाला स्कैम पोस्ट किया।",
            "impact": "कुछ ही घंटों में स्कैम से 1 लाख डॉलर से ज़्यादा के बिटकॉइन कमाए गए, और यह उजागर हुआ कि सिर्फ एक फोन कॉल कैसे किसी बड़े प्लेटफॉर्म को खतरे में डाल सकता है।",
            "lesson": "सुरक्षा की सबसे कमज़ोर कड़ी अक्सर फोन पर मौजूद इंसान होता है, फायरवॉल नहीं। किसी को भी एक्सेस देने से पहले पहचान वेरीफाई करना सिखाएं।",
        },
    },
    {
        "title": "Colonial Pipeline Ransomware Attack",
        "year": 2021,
        "en": {
            "what": "A single compromised VPN password, reused from another breach and lacking multi-factor authentication, gave DarkSide ransomware operators entry.",
            "method": "Once inside, they deployed ransomware across Colonial Pipeline's billing systems, forcing the company to shut down the pipeline as a precaution.",
            "impact": "The largest fuel pipeline in the US went offline, causing panic-buying and fuel shortages across the East Coast, and a $4.4M ransom payment.",
            "lesson": "One reused password without MFA took down critical national infrastructure. MFA on every remote access point is non-negotiable.",
        },
        "hi": {
            "what": "एक ऐसा VPN पासवर्ड जो पहले किसी और ब्रीच में लीक हो चुका था और जिस पर मल्टी-फैक्टर ऑथेंटिकेशन नहीं था, उसी से DarkSide रैंसमवेयर ऑपरेटरों को एंट्री मिली।",
            "method": "अंदर घुसते ही उन्होंने Colonial Pipeline के बिलिंग सिस्टम में रैंसमवेयर फैला दिया, जिससे कंपनी को एहतियातन पूरी पाइपलाइन बंद करनी पड़ी।",
            "impact": "अमेरिका की सबसे बड़ी फ्यूल पाइपलाइन ठप हो गई, जिससे पूर्वी तट पर पेट्रोल की किल्लत और पैनिक-बाइंग मच गई, और कंपनी ने 44 लाख डॉलर की फिरौती चुकाई।",
            "lesson": "बिना MFA के एक दोबारा इस्तेमाल किए गए पासवर्ड ने देश के महत्वपूर्ण इंफ्रास्ट्रक्चर को ठप कर दिया। हर रिमोट एक्सेस पॉइंट पर MFA अनिवार्य होना चाहिए।",
        },
    },
    {
        "title": "The Ashley Madison Breach",
        "year": 2015,
        "en": {
            "what": "A hacktivist group calling itself 'Impact Team' breached the servers of an affair-focused dating site over data-ethics objections.",
            "method": "They exfiltrated the full user database and, when the company refused to shut the site down, leaked over 30 million users' personal data.",
            "impact": "Real names, addresses, and payment details were exposed, leading to extortion attempts, public shaming, divorces, and reported suicides.",
            "lesson": "Any platform holding sensitive personal data is a target. Data minimization and strong encryption aren't optional for sensitive services.",
        },
        "hi": {
            "what": "'Impact Team' नाम के एक हैक्टिविस्ट ग्रुप ने डेटा-नैतिकता को लेकर आपत्ति जताते हुए एक अफेयर-केंद्रित डेटिंग साइट के सर्वर हैक कर लिए।",
            "method": "उन्होंने पूरा यूज़र डेटाबेस चुरा लिया और जब कंपनी ने साइट बंद करने से इनकार किया, तो 3 करोड़ से ज़्यादा यूज़र्स का निजी डेटा लीक कर दिया।",
            "impact": "असली नाम, पते और पेमेंट जानकारी उजागर हुई, जिससे जबरन वसूली, सार्वजनिक बदनामी, तलाक और आत्महत्या के मामले भी सामने आए।",
            "lesson": "संवेदनशील निजी डेटा रखने वाला कोई भी प्लेटफॉर्म एक लक्ष्य है। संवेदनशील सेवाओं के लिए डेटा मिनिमाइज़ेशन और मज़बूत एन्क्रिप्शन ज़रूरी है, विकल्प नहीं।",
        },
    },
    {
        "title": "SolarWinds Supply Chain Attack",
        "year": 2020,
        "en": {
            "what": "State-sponsored actors quietly inserted malicious code into a routine software update for SolarWinds' Orion network management platform.",
            "method": "Any organization that installed the trusted update unknowingly gave the attackers a backdoor into their own network.",
            "impact": "Roughly 18,000 organizations were compromised, including multiple US federal agencies, undetected for close to a year.",
            "lesson": "Trust in your software supply chain isn't automatic. Vet vendors, monitor for anomalous behavior even from 'trusted' updates.",
        },
        "hi": {
            "what": "किसी देश-प्रायोजित समूह ने चुपचाप SolarWinds के Orion नेटवर्क मैनेजमेंट सॉफ़्टवेयर के एक सामान्य अपडेट में मैलिशियस कोड डाल दिया।",
            "method": "जिस भी संगठन ने उस भरोसेमंद अपडेट को इंस्टॉल किया, उसने अनजाने में हमलावरों को अपने नेटवर्क का बैकडोर दे दिया।",
            "impact": "लगभग 18,000 संगठन प्रभावित हुए, जिनमें अमेरिका की कई संघीय एजेंसियां भी शामिल थीं, और यह हमला करीब एक साल तक पकड़ में नहीं आया।",
            "lesson": "अपनी सॉफ़्टवेयर सप्लाई चेन पर भरोसा अपने आप नहीं बनता। वेंडर की जांच करें और 'भरोसेमंद' अपडेट्स में भी असामान्य गतिविधि पर नज़र रखें।",
        },
    },
    {
        "title": "The Mt. Gox Bitcoin Heist",
        "year": 2014,
        "en": {
            "what": "The world's largest Bitcoin exchange at the time was slowly bled dry by attackers who had compromised a private key years earlier.",
            "method": "Small, undetected withdrawals drained the exchange's wallets over an extended period before anyone noticed the scale of the theft.",
            "impact": "850,000 BTC vanished, wiping out most customer holdings overnight and triggering the exchange's collapse.",
            "lesson": "Never leave large amounts of crypto on an exchange. Cold storage and regular wallet audits catch slow leaks before they become catastrophic.",
        },
        "hi": {
            "what": "उस समय की दुनिया की सबसे बड़ी बिटकॉइन एक्सचेंज को हमलावरों ने धीरे-धीरे खाली कर दिया, जिन्होंने वर्षों पहले एक प्राइवेट की चुरा ली थी।",
            "method": "छोटी-छोटी, अनदेखी निकासियों ने लंबे समय तक एक्सचेंज के वॉलेट्स को खाली किया, इससे पहले कि किसी को चोरी की गंभीरता का पता चलता।",
            "impact": "8.5 लाख BTC गायब हो गए, जिससे रातोंरात ज़्यादातर ग्राहकों की जमा पूंजी खत्म हो गई और एक्सचेंज ध्वस्त हो गई।",
            "lesson": "एक्सचेंज पर बड़ी मात्रा में क्रिप्टो कभी न रखें। कोल्ड स्टोरेज और नियमित वॉलेट ऑडिट धीमी चोरी को तबाही बनने से पहले पकड़ लेते हैं।",
        },
    },
    {
        "title": "Indian Data Leak Pattern — Misconfigured Databases",
        "year": 2021,
        "en": {
            "what": "A recurring pattern across Indian services: misconfigured cloud databases and third-party vendor leaks exposing citizens' personal records.",
            "method": "Databases left open without authentication, or vendors with weak security handling sensitive data, allowed researchers and attackers alike to access records.",
            "impact": "Hundreds of millions of records — names, phone numbers, addresses — exposed across multiple incidents over the years.",
            "lesson": "Always check who your data is shared with, and whether services follow basic security hygiene like authentication on databases.",
        },
        "hi": {
            "what": "भारतीय सेवाओं में एक बार-बार दिखने वाला पैटर्न: गलत तरीके से कॉन्फ़िगर किए गए क्लाउड डेटाबेस और थर्ड-पार्टी वेंडर लीक, जिनसे नागरिकों का निजी डेटा उजागर हुआ।",
            "method": "बिना ऑथेंटिकेशन के खुले छोड़े गए डेटाबेस, या कमज़ोर सुरक्षा वाले वेंडरों के पास मौजूद संवेदनशील डेटा — दोनों ने रिसर्चरों और हमलावरों दोनों को रिकॉर्ड्स तक पहुंच दी।",
            "impact": "वर्षों में कई घटनाओं में करोड़ों रिकॉर्ड्स — नाम, फोन नंबर, पते — उजागर हुए।",
            "lesson": "हमेशा जांचें कि आपका डेटा किसके साथ साझा किया जा रहा है, और क्या सेवाएं डेटाबेस पर ऑथेंटिकेशन जैसी बुनियादी सुरक्षा का पालन करती हैं।",
        },
    },
]

SECURITY_TIPS = [
    {
        "en": "Enable app-based 2FA (not SMS) on every account that supports it — SIM swap attacks bypass SMS OTPs easily.",
        "hi": "जहां भी संभव हो, SMS की बजाय ऐप-आधारित 2FA चालू करें — SIM स्वैप अटैक से SMS OTP आसानी से बायपास हो जाता है।",
    },
    {
        "en": "Never reuse passwords across sites. A breach on one throws away the lock on all of them.",
        "hi": "किसी भी दो वेबसाइट पर एक जैसा पासवर्ड इस्तेमाल न करें। एक जगह डेटा लीक होने से बाकी सभी अकाउंट्स का ताला भी टूट जाता है।",
    },
    {
        "en": "Check URLs character-by-character before entering credentials — 'rnicrosoft.com' isn't microsoft.com.",
        "hi": "लॉगिन जानकारी डालने से पहले URL को ध्यान से पढ़ें — 'rnicrosoft.com', microsoft.com नहीं है।",
    },
    {
        "en": "Update your router firmware. Most home IoT botnets exploit routers still on factory defaults.",
        "hi": "अपने राउटर का फर्मवेयर अपडेट रखें। ज़्यादातर घरेलू IoT बॉटनेट फैक्ट्री-डिफ़ॉल्ट सेटिंग वाले राउटरों को ही निशाना बनाते हैं।",
    },
    {
        "en": "Public Wi-Fi + no VPN = anyone on the network can potentially see your traffic.",
        "hi": "पब्लिक वाई-फाई + बिना VPN के इस्तेमाल का मतलब है कि नेटवर्क पर मौजूद कोई भी आपका डेटा ट्रैफिक देख सकता है।",
    },
    {
        "en": "Verify unexpected 'urgent' requests (money transfer, gift cards, password reset) via a second channel before acting.",
        "hi": "अचानक आई 'अर्जेंट' मांगों (पैसे ट्रांसफर, गिफ्ट कार्ड, पासवर्ड रीसेट) को मानने से पहले किसी दूसरे माध्यम से पुष्टि ज़रूर करें।",
    },
    {
        "en": "Freeze your credit report if your country supports it — stops most identity-theft loan fraud cold.",
        "hi": "अगर आपके देश में यह सुविधा है, तो अपनी क्रेडिट रिपोर्ट फ्रीज़ करें — इससे पहचान चोरी से होने वाले लोन फ्रॉड रुक जाते हैं।",
    },
    {
        "en": "Back up important data offline (3-2-1 rule) — the only reliable ransomware insurance.",
        "hi": "ज़रूरी डेटा का ऑफलाइन बैकअप रखें (3-2-1 नियम) — रैंसमवेयर से बचने का यही सबसे भरोसेमंद तरीका है।",
    },
]

# Bug bounty / VAPT methodology tips — standard public knowledge (OWASP Testing
# Guide, PortSwigger Academy style content). General technique + a common tool
# command, no target-specific exploitation. Always practice only on
# authorized scope (bug bounty programs, labs, or your own systems).
BUG_BOUNTY_TIPS = [
    {
        "category": "Recon",
        "en_tip": "Start every engagement with subdomain enumeration before touching the main app — forgotten staging subdomains are where the easy wins live.",
        "hi_tip": "किसी भी engagement की शुरुआत हमेशा subdomain enumeration से करें — भुला दिए गए staging subdomains में अक्सर सबसे आसान bugs मिलते हैं।",
        "command": "subfinder -d target.com -silent | httpx -silent -status-code",
    },
    {
        "category": "IDOR",
        "en_tip": "When testing IDOR, don't just change the ID — try swapping it with another valid user's ID from a different account you control, not just incrementing/decrementing.",
        "hi_tip": "IDOR टेस्ट करते समय सिर्फ ID बदलना काफी नहीं — किसी दूसरे अकाउंट के असली ID से स्वैप करके भी टेस्ट करें, सिर्फ बढ़ाना-घटाना ही काफी नहीं।",
        "command": "ffuf -u https://target.com/api/user/FUZZ -w ids.txt -H 'Authorization: Bearer <token>'",
    },
    {
        "category": "XSS",
        "en_tip": "Reflected XSS filters often only block <script> tags. Test with event handlers and non-standard tags before giving up on an input.",
        "hi_tip": "Reflected XSS filters अक्सर सिर्फ <script> टैग को ब्लॉक करते हैं। किसी input को छोड़ने से पहले event handlers और गैर-मानक टैग से भी टेस्ट करें।",
        "command": "<svg onload=alert(document.domain)>  /  \"><img src=x onerror=alert(1)>",
    },
    {
        "category": "SQLi",
        "en_tip": "Time-based blind SQLi is often missed by scanners. If a query returns identical output regardless of input, always test for timing differences.",
        "hi_tip": "Time-based blind SQLi को अक्सर scanners मिस कर देते हैं। अगर output हर बार एक जैसा दिखे, तो timing में फर्क ज़रूर टेस्ट करें।",
        "command": "' AND SLEEP(5)-- -   /   sqlmap -u \"https://target.com/item?id=1\" --technique=T",
    },
    {
        "category": "Recon",
        "en_tip": "Directory/parameter brute-forcing on JS files often reveals hidden API endpoints that were never meant to be public.",
        "hi_tip": "JS files पर directory/parameter brute-forcing करने से अक्सर hidden API endpoints मिल जाते हैं जो कभी public नहीं होने चाहिए थे।",
        "command": "katana -u https://target.com -jc | grep -Eo '\\/[a-zA-Z0-9_/-]*\\.js' | sort -u",
    },
    {
        "category": "Access Control",
        "en_tip": "Always test the same request as a lower-privilege role AND as a completely unauthenticated user — broken access control bugs love role-downgrade edge cases.",
        "hi_tip": "हमेशा एक ही request को low-privilege role से और बिना login के भी टेस्ट करें — broken access control bugs role-downgrade edge cases में ही सबसे ज़्यादा मिलते हैं।",
        "command": "curl -X GET https://target.com/api/admin/users -H 'Authorization: Bearer <low_priv_token>'",
    },
    {
        "category": "SSRF",
        "en_tip": "When a target's URL/image-fetch feature exists, always test cloud metadata endpoints — this single bug class has led to full cloud account takeovers.",
        "hi_tip": "अगर किसी target में URL/image-fetch वाला feature है, तो cloud metadata endpoints ज़रूर टेस्ट करें — इसी एक bug class से पूरे cloud account takeover हो चुके हैं।",
        "command": "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
    },
    {
        "category": "Recon",
        "en_tip": "Check GitHub/GitLab for leaked API keys and .env files from a target's employees or old repos — one of the highest-value, lowest-effort bug bounty finds.",
        "hi_tip": "किसी target के employees या पुराने repos में leaked API keys और .env files के लिए GitHub/GitLab ज़रूर चेक करें — यह सबसे ज़्यादा value वाला और सबसे कम मेहनत वाला bug bounty find है।",
        "command": "trufflehog github --org=targetorg --only-verified",
    },
    {
        "category": "Business Logic",
        "en_tip": "Automated scanners can't find business logic flaws — always manually walk through checkout/payment/coupon flows trying to reorder or repeat steps.",
        "hi_tip": "Automated scanners business logic flaws नहीं ढूंढ सकते — checkout/payment/coupon flows को मैन्युअली, कदम दोहराकर या क्रम बदलकर ज़रूर टेस्ट करें।",
        "command": "Manual testing only — no single command replaces walking the flow yourself.",
    },
    {
        "category": "Recon",
        "en_tip": "Always check for exposed .git directories on a target — a full source code leak is one of the most severe findings you can report.",
        "hi_tip": "किसी target पर exposed .git directory ज़रूर चेक करें — पूरा source code leak होना सबसे गंभीर findings में से एक होता है।",
        "command": "curl -s https://target.com/.git/HEAD",
    },
]
