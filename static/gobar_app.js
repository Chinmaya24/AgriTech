// AgriAI+ Gobar Gas Platform - Corrected Modular JS
// Single-file frontend logic (vanilla JS)

(function(){
  // --- State ---
  let currentLang = 'en';
  let currentPage = 'home';
  let greenCredits = 0;
  let marketEntries = [];
  let claimedEntries = [];
  let communityEntries = [];

  // --- Translations (cleaned; includes en, hi, kn, ta, bn) ---
  const translations = {
    en: {
      nav: ["Home", "About Us", "Contact Us"],
  sidebar: ["Dashboard", "Gobar Gas Calculator", "Biogas Savings Calculator", "C2F Connect", "Wet Waste Portal", "Crop Guidance", "Knowledge Hub"],
      home: {
        heroTitle: "What is Gobar Gas?",
        heroDesc: "Gobar gas is biogas produced from cattle dung and organic waste. It is a renewable energy source for sustainable farming.",
        learnMore: "Learn More",
        videoLabel: "Watch: Gobar Gas Explained"
      },
      about: "AgriAI+ is a farmer-first platform for sustainable agriculture and renewable energy.",
      contact: "Contact us at support@agriai.com or call 1800-AGRI-AI.",
      calc: {
        title: "Gobar Gas Calculator",
        label: "Enter amount of organic waste (kg)",
        btn: "Calculate",
        output: ["Biogas produced (m³/day)", "LPG equivalent (kg)", "Electricity produced (kWh)", "CO₂ reduced (kg)"]
      },

      c2f: {
        title: "Customer-to-Farmer Connect",
        available: "Available Waste Entries",
        claimed: "Claimed Waste Entries",
        claimBtn: "Claim"
      },
      wetwaste: {
        title: "Wet Waste Portal",
        form: ["Restaurant Name", "Waste Type", "Quantity (kg)", "Location", "Submit Waste"],
        types: ["Cow Dung", "Wet Waste", "Other"]
      },
      crop: {
        title: "Crop Guidance",
        tableHead: ["Crop", "Slurry (kg/acre)", "Effluent (L/acre)"]
      },
      knowledge: {
        title: "Knowledge Hub",
        articles: [
          {title: "Benefits of Gobar Gas", text: "Gobar gas reduces fossil fuel use and improves soil health.", video: "https://www.youtube.com/embed/VIDEO_ID1"},
          {title: "Composting Techniques", text: "Learn how to compost organic waste for better yields.", video: "https://www.youtube.com/embed/VIDEO_ID2"},
          {title: "Water Conservation", text: "Tips for saving water in agriculture.", video: ""}
        ]
      },
      dashboard: {
        title: "Dashboard",
        credits: "Green Credits",
        weather: "Weather Today"
      },
      successStories: [
        {img: "https://t3.ftcdn.net/jpg/04/32/15/18/360_F_432151892_oQ3YQDo2LYZPILlEMnlo55PjjgiUwnQb.jpg", quote: "Gobar gas changed my farm!", name: "Ravi Kumar"},
        {img: "https://eatrevolutionindia.com/wp-content/uploads/2025/05/farmers-empowerment.jpg", quote: "Now I save on LPG every month.", name: "Lakshmi Devi"},
        {img: "https://static.vecteezy.com/system/resources/thumbnails/025/228/033/small_2x/indian-happy-farmer-holding-green-chilli-green-chilli-farming-young-farmer-photo.jpg", quote: "My crops are healthier with slurry.", name: "Manoj Singh"}
      ]
    },
    hi: {
      nav: ["होम", "हमारे बारे में", "संपर्क करें"],
      sidebar: ["डैशबोर्ड", "गोबर गैस कैलकुलेटर", "C2F कनेक्ट", "वेट वेस्ट पोर्टल", "फसल मार्गदर्शन", "नॉलेज हब", "बायोगैस बचत"],
      home: { heroTitle: "गोबर गैस क्या है?", heroDesc: "गोबर गैस पशु अपशिष्ट और जैविक कचरे से उत्पन्न बायोगैस है। यह सतत कृषि के लिए अक्षय ऊर्जा स्रोत है।", learnMore: "और जानें", videoLabel: "देखें: गोबर गैस समझाया गया" },
      about: "AgriAI+ किसानों के लिए सतत कृषि और अक्षय ऊर्जा का प्लेटफार्म है।",
      contact: "हमसे संपर्क करें support@agriai.com या 1800-AGRI-AI पर।",
      calc: { title: "गोबर गैस कैलकुलेटर", label: "जैविक अपशिष्ट की मात्रा दर्ज करें (किग्रा)", btn: "गणना करें", output: ["उत्पादित बायोगैस (m³/दिन)", "एलपीजी समतुल्य (किग्रा)", "उत्पादित बिजली (कWh)", "CO₂ में कमी (किग्रा)"] },
      biogasSavings: {
        title: "बायोगैस बचत कैलकुलेटर",
        biogasInput: "उत्पादित बायोगैस (m³/माह):",
        lpgPriceInput: "एलपीजी मूल्य (₹/किग्रा):",
        btn: "बचत की गणना करें",
        howItWorks: "यह कैसे काम करता है?",
        list: ["एलपीजी समतुल्य = बायोगैस × 0.43 (किग्रा एलपीजी)", "बचाया गया पैसा = एलपीजी समतुल्य × एलपीजी मूल्य", "बचाया गया CO₂ = एलपीजी समतुल्य × 2.9 (किग्रा)"],
        resultDesc: {
          money: "मासिक बचाया गया पैसा",
          co2: "बचाया गया CO₂"
        }
      },
      c2f: { title: "कस्टमर-टू-फार्मर कनेक्ट", available: "उपलब्ध अपशिष्ट प्रविष्टियाँ", claimed: "क्लेम की गई प्रविष्टियाँ", claimBtn: "क्लेम करें" },
      wetwaste: { title: "वेट वेस्ट पोर्टल", form: ["रेस्टोरेंट नाम", "अपशिष्ट प्रकार", "मात्रा (किग्रा)", "स्थान", "अपशिष्ट सबमिट करें"], types: ["गोबर", "वेट वेस्ट", "अन्य"] },
      crop: { title: "फसल मार्गदर्शन", tableHead: ["फसल", "स्लरी (किग्रा/एकड़)", "एफ्लुएंट (लीटर/एकड़)"] },
      knowledge: { title: "नॉलेज हब", articles: [ {title: "गोबर गैस के लाभ", text: "गोबर गैस जीवाश्म ईंधन का उपयोग कम करता है और मिट्टी की गुणवत्ता बढ़ाता है।", video: "https://www.youtube.com/embed/VIDEO_ID1"}, {title: "कम्पोस्टिंग तकनीक", text: "बेहतर उपज के लिए जैविक कचरे की कम्पोस्टिंग सीखें।", video: "https://www.youtube.com/embed/VIDEO_ID2"}, {title: "जल संरक्षण", text: "कृषि में पानी बचाने के टिप्स।", video: "" } ] },
      dashboard: { title: "डैशबोर्ड", credits: "ग्रीन क्रेडिट्स", weather: "आज का मौसम" },
      successStories: [ {img: "assets/farmer1.jpg", quote: "गोबर गैस ने मेरी खेती बदल दी!", name: "रवि कुमार"}, {img: "assets/farmer2.jpg", quote: "अब हर महीने LPG की बचत होती है।", name: "लक्ष्मी देवी"}, {img: "assets/farmer3.jpg", quote: "स्लरी से मेरी फसलें स्वस्थ हैं।", name: "मनोज सिंह" } ]
    },
    kn: {
      nav: ["ಮುಖಪುಟ", "ನಮ್ಮ ಬಗ್ಗೆ", "ಸಂಪರ್ಕ"],
      sidebar: ["ಡ್ಯಾಶ್‌ಬೋರ್ಡ್", "ಗೋಬರ್ ಗ್ಯಾಸ್ ಕ್ಯಾಲ್ಕುಲೇಟರ್", "C2F ಸಂಪರ್ಕ", "ವೆಟ್ ವೆಸ್ಟ್ ಪೋರ್ಟಲ್", "ಬೆಳೆ ಮಾರ್ಗದರ್ಶನ", "ನಾಲೆಜ್ ಹಬ್", "ಬಯೋಗ್ಯಾಸ್ ಉಳಿತಾಯ"],
      home: { heroTitle: "ಗೋಬರ್ ಗ್ಯಾಸ್ ಎಂದರೇನು?", heroDesc: "ಗೋಬರ್ ಗ್ಯಾಸ್ ಎಂಬುದು ಹಸುಮಲ ಮತ್ತು ಸಸ್ಯಜ ತ್ಯಾಜ್ಯದಿಂದ ಉತ್ಪಾದಿಸುವ ಬಯೋಗ್ಯಾಸ್ ಆಗಿದೆ. ಇದು ಸ್ಥಿರ ಕೃಷಿಗೆ ನವೀಕೃತ ಶಕ್ತಿಯ ಮೂಲವಾಗಿದೆ.", learnMore: "ಇನ್ನಷ್ಟು ತಿಳಿಯಿರಿ", videoLabel: "ನೋಡಿ: ಗೋಬರ್ ಗ್ಯಾಸ್ ವಿವರಣೆ" },
      about: "AgriAI+ ಸ್ಥಿರ ಕೃಷಿ ಮತ್ತು ನವೀಕೃತ ಶಕ್ತಿಗೆ ರೈತರಿಗಾಗಿ ವೇದಿಕೆ.",
      contact: "support@agriai.com ಗೆ ಸಂಪರ್ಕಿಸಿ ಅಥವಾ 1800-AGRI-AI ಗೆ ಕರೆ ಮಾಡಿ.",
      calc: { title: "ಗೋಬರ್ ಗ್ಯಾಸ್ ಕ್ಯಾಲ್ಕುಲೇಟರ್", label: "ಸಸ್ಯಜ ತ್ಯಾಜ್ಯ ಪ್ರಮಾಣವನ್ನು ನಮೂದಿಸಿ (ಕೆಜಿ)", btn: "ಗಣನೆ ಮಾಡಿ", output: ["ಉತ್ಪಾದಿತ ಬಯೋಗ್ಯಾಸ್ (m³/ದಿನ)", "LPG ಸಮಾನ (ಕೆಜಿ)", "ಉತ್ಪಾದಿತ ವಿದ್ಯುತ್ (kWh)", "CO₂ ಕಡಿತ (ಕೆಜಿ)"] },
      biogasSavings: {
        title: "ಬಯೋಗ್ಯಾಸ್ ಉಳಿತಾಯ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        biogasInput: "ಉತ್ಪಾದಿತ ಬಯೋಗ್ಯಾಸ್ (m³/ತಿಂಗಳು):",
        lpgPriceInput: "LPG ಬೆಲೆ (₹/ಕೆಜಿ):",
        btn: "ಉಳಿತಾಯ ಗಣನೆ ಮಾಡಿ",
        howItWorks: "ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ?",
        list: ["LPG ಸಮಾನ = ಬಯೋಗ್ಯಾಸ್ × 0.43 (ಕೆಜಿ LPG)", "ಉಳಿಸಿದ ಹಣ = LPG ಸಮಾನ × LPG ಬೆಲೆ", "ಉಳಿಸಿದ CO₂ = LPG ಸಮಾನ × 2.9 (ಕೆಜಿ)"],
        resultDesc: {
          money: "ಮಾಸಿಕ ಉಳಿಸಿದ ಹಣ",
          co2: "ಉಳಿಸಿದ CO₂"
        }
      },
      c2f: { title: "ಗ್ರಾಹಕ-ರೈತ ಸಂಪರ್ಕ", available: "ಲಭ್ಯವಿರುವ ತ್ಯಾಜ್ಯ ಎಂಟ್ರಿಗಳು", claimed: "ಕ್ಲೈಮ್ ಮಾಡಿದ ಎಂಟ್ರಿಗಳು", claimBtn: "ಕ್ಲೈಮ್ ಮಾಡಿ" },
      wetwaste: { title: "ವೆಟ್ ವೆಸ್ಟ್ ಪೋರ್ಟಲ್", form: ["ಹೋಟೆಲ್ ಹೆಸರು", "ತ್ಯಾಜ್ಯ ಪ್ರಕಾರ", "ಪ್ರಮಾಣ (ಕೆಜಿ)", "ಸ್ಥಳ", "ತ್ಯಾಜ್ಯ ಸಲ್ಲಿಸಿ"], types: ["ಹಸುಮಲ", "ವೆಟ್ ವೆಸ್ಟ್", "ಇತರೆ"] },
      crop: { title: "ಬೆಳೆ ಮಾರ್ಗದರ್ಶನ", tableHead: ["ಬೆಳೆ", "ಸ್ಲರಿ (ಕೆಜಿ/ಎಕರೆ)", "ಎಫ್ಲುವೆಂಟ್ (ಲೀ/ಎಕರೆ)"] },
      knowledge: { title: "ನಾಲೆಜ್ ಹಬ್", articles: [ {title: "ಗೋಬರ್ ಗ್ಯಾಸ್ ಪ್ರಯೋಜನಗಳು", text: "ಗೋಬರ್ ಗ್ಯಾಸ್ ಇಂಧನ ಬಳಕೆಯನ್ನು ಕಡಿಮೆ ಮಾಡುತ್ತದೆ ಮತ್ತು ನೆಲದ ಆರೋಗ್ಯವನ್ನು ಸುಧಾರಿಸುತ್ತದೆ.", video: "https://www.youtube.com/embed/VIDEO_ID1"}, {title: "ಕಂಪೋಸ್ಟಿಂಗ್ ತಂತ್ರಗಳು", text: "ಉತ್ತಮ ಬೆಳೆಗೆ ಸಸ್ಯಜ ತ್ಯಾಜ್ಯವನ್ನು ಕಂಪೋಸ್ಟ್ ಮಾಡುವುದನ್ನು ಕಲಿಯಿರಿ.", video: "https://www.youtube.com/embed/VIDEO_ID2"}, {title: "ನೀರು ಸಂರಕ್ಷಣೆ", text: "ಕೃಷಿಯಲ್ಲಿ ನೀರನ್ನು ಉಳಿಸುವ ಸಲಹೆಗಳು.", video: "" } ] },
      dashboard: { title: "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್", credits: "ಹಸಿರು ಕ್ರೆಡಿಟ್ಸ್", weather: "ಇಂದಿನ ಹವಾಮಾನ" },
      successStories: [ {img: "assets/farmer1.jpg", quote: "ಗೋಬರ್ ಗ್ಯಾಸ್ ನನ್ನ ಕೃಷಿಯನ್ನು ಬದಲಾಯಿಸಿದೆ!", name: "ರವಿಕುಮಾರ್"}, {img: "assets/farmer2.jpg", quote: "ಪ್ರತಿ ತಿಂಗಳು LPG ಉಳಿಸುತ್ತೇನೆ.", name: "ಲಕ್ಷ್ಮೀ ದೇವಿ"}, {img: "assets/farmer3.jpg", quote: "ಸ್ಲರಿ ಬಳಕೆದಿಂದ ಬೆಳೆಗಳು ಆರೋಗ್ಯವಾಗಿವೆ.", name: "ಮನುಜ್ ಸಿಂಗ್" } ]
    },
    ta: {
      nav: ["முகப்பு", "எங்களை பற்றி", "தொடர்பு"],
      sidebar: ["டாஷ்போர்டு", "கோபர் கேஸ் கணிப்பான்", "C2F இணைப்பு", "ஈரமான கழிவு போர்டல்", "விவசாய வழிகாட்டி", "அறிவு மையம்", "பயோகாஸ் சேமிப்பு"],
      home: { heroTitle: "கோபர் கேஸ் என்றால் என்ன?", heroDesc: "கோபர் கேஸ் என்பது மாட்டின் கழிவும், உயிர் கழிவும் கொண்டு தயாரிக்கப்படும் பயோகாஸ். இது நிலையான விவசாயத்திற்கு புதுப்பிக்கக்கூடிய சக்தி ஆதாரம்.", learnMore: "மேலும் அறிக", videoLabel: "பார்க்க: கோபர் கேஸ் விளக்கம்" },
      about: "AgriAI+ நிலையான விவசாயம் மற்றும் புதுப்பிக்கக்கூடிய சக்திக்கு விவசாயிகளுக்கான தளம்.",
      contact: "support@agriai.com-ஐ தொடர்பு கொள்ளவும் அல்லது 1800-AGRI-AI-ஐ அழைக்கவும்.",
      calc: { title: "கோபர் கேஸ் கணிப்பான்", label: "உயிர் கழிவு அளவை உள்ளிடவும் (கிலோ)", btn: "கணக்கிடு", output: ["உற்பத்தி செய்யப்பட்ட பயோகாஸ் (m³/நாள்)", "LPG சமம் (கிலோ)", "உற்பத்தி செய்யப்பட்ட மின்சாரம் (kWh)", "CO₂ குறைவு (கிலோ)"] },
      biogasSavings: {
        title: "பயோகாஸ் சேமிப்பு கணிப்பான்",
        biogasInput: "உற்பத்தி செய்யப்பட்ட பயோகாஸ் (m³/மாதம்):",
        lpgPriceInput: "LPG விலை (₹/கிலோ):",
        btn: "சேமிப்பை கணக்கிடு",
        howItWorks: "இது எவ்வாறு வேலை செய்கிறது?",
        list: ["LPG சமம் = பயோகாஸ் × 0.43 (கிலோ LPG)", "சேமிக்கப்பட்ட பணம் = LPG சமம் × LPG விலை", "சேமிக்கப்பட்ட CO₂ = LPG சமம் × 2.9 (கிலோ)"],
        resultDesc: {
          money: "மாதாந்திர சேமிக்கப்பட்ட பணம்",
          co2: "சேமிக்கப்பட்ட CO₂"
        }
      },
      c2f: { title: "வாடிக்கையாளர்-விவசாயி இணைப்பு", available: "கிடைக்கும் கழிவு பதிவுகள்", claimed: "கிளைம் செய்யப்பட்ட பதிவுகள்", claimBtn: "கிளைம் செய்" },
      wetwaste: { title: "ஈரமான கழிவு போர்டல்", form: ["உணவகம் பெயர்", "கழிவு வகை", "அளவு (கிலோ)", "இடம்", "கழிவு சமர்ப்பிக்கவும்"], types: ["மாட்டு கழிவு", "ஈரமான கழிவு", "மற்றவை"] },
      crop: { title: "விவசாய வழிகாட்டி", tableHead: ["பயிர்", "சலரி (கிலோ/ஏக்கர்)", "எஃப்ளூஎண்ட் (லிட்டர்/ஏக்கர்)"] },
      knowledge: { title: "அறிவு மையம்", articles: [ {title: "கோபர் கேஸ் நன்மைகள்", text: "கோபர் கேஸ் எரிவாயு பயன்பாட்டை குறைக்கிறது மற்றும் மண்ணின் ஆரோக்கியத்தை மேம்படுத்துகிறது.", video: "https://www.youtube.com/embed/VIDEO_ID1"}, {title: "கம்போஸ்டிங் நுட்பங்கள்", text: "சிறந்த விளைச்சலுக்கு உயிர் கழிவை கம்போஸ்ட் செய்வது எப்படி என்பதை அறிக.", video: "https://www.youtube.com/embed/VIDEO_ID2"}, {title: "நீர் பாதுகாப்பு", text: "விவசாயத்தில் நீரை சேமிக்க உதவும் குறிப்புகள்.", video: "" } ] },
      dashboard: { title: "டாஷ்போர்டு", credits: "பசுமை கிரெடிட்ஸ்", weather: "இன்றைய வானிலை" },
      successStories: [ {img: "assets/farmer1.jpg", quote: "கோபர் கேஸ் என் விவசாயத்தை மாற்றியது!", name: "ரவிகுமார்"}, {img: "assets/farmer2.jpg", quote: "ஒவ்வொரு மாதமும் LPG சேமிக்கிறேன்.", name: "லட்சுமி தேவி"}, {img: "assets/farmer3.jpg", quote: "சலரி மூலம் பயிர்கள் ஆரோக்கியமாக உள்ளன.", name: "மனோஜ் சிங்" } ]
    },
    bn: {
      nav: ["হোম", "আমাদের সম্পর্কে", "যোগাযোগ করুন"],
      sidebar: ["ড্যাশবোর্ড", "গোবর গ্যাস ক্যালকুলেটর", "C2F সংযোগ", "ভেজা বর্জ্য পোর্টাল", "ফসল নির্দেশিকা", "জ্ঞান কেন্দ্র", "বায়োগ্যাস সঞ্চয়"],
      home: { heroTitle: "গোবর গ্যাস কী?", heroDesc: "গোবর গ্যাস হল গবাদি পশুর গোবর এবং জৈব বর্জ্য থেকে উৎপাদিত বায়োগ্যাস। এটি টেকসই কৃষির জন্য একটি পুনর্নবীকরণযোগ্য শক্তি উৎস।", learnMore: "আরও জানুন", videoLabel: "দেখুন: গোবর গ্যাস ব্যাখ্যা" },
      about: "AgriAI+ কৃষকদের জন্য টেকসই কৃষি এবং পুনর্নবীকরণযোগ্য শক্তির প্ল্যাটফর্ম।",
      contact: "যোগাযোগ করুন support@agriai.com অথবা 1800-AGRI-AI-এ।",
      calc: { title: "গোবর গ্যাস ক্যালকুলেটর", label: "জৈব বর্জ্যের পরিমাণ লিখুন (কেজি)", btn: "গণনা করুন", output: ["উৎপাদিত বায়োগ্যাস (m³/দিন)", "LPG সমতুল্য (কেজি)", "উৎপাদিত বিদ্যৎ (kWh)", "CO₂ হ্রাস (কেজি)"] },
      biogasSavings: {
        title: "বায়োগ্যাস সঞ্চয় ক্যালকুলেটর",
        biogasInput: "উৎপাদিত বায়োগ্যাস (m³/মাস):",
        lpgPriceInput: "এলপিজি মূল্য (₹/কেজি):",
        btn: "সঞ্চয় গণনা করুন",
        howItWorks: "এটি কীভাবে কাজ করে?",
        list: ["এলপিজি সমতুল্য = বায়োগ্যাস × 0.43 (কেজি এলপিজি)", "সঞ্চয়কৃত অর্থ = এলপিজি সমতুল্য × এলপিজি মূল্য", "সঞ্চয়কৃত CO₂ = এলপিজি সমতুল্য × 2.9 (কেজি)"],
        resultDesc: {
          money: "মাসিক সঞ্চয়কৃত অর্থ",
          co2: "সঞ্চয়কৃত CO₂"
        }
      },
      c2f: { title: "গ্রাহক-টু-চাষি সংযোগ", available: "উপলব্ধ বর্জ্য এন্ট্রি", claimed: "ক্লেইমকৃত এন্ট্রি", claimBtn: "ক্লেইম করুন" },
      wetwaste: { title: "ভেজা বর্জ্য পোর্টাল", form: ["রেস্টুরেন্ট নাম", "বর্জ্যের ধরন", "পরিমাণ (কেজি)", "অবস্থান", "বর্জ্য জমা দিন"], types: ["গোবর", "ভেজা বর্জ্য", "অন্যান্য"] },
      crop: { title: "ফসল নির্দেশিকা", tableHead: ["ফসল", "স্লারি (কেজি/একর)", "এফ্লুয়েন্ট (লিটার/একর)"] },
      knowledge: { title: "জ্ঞান কেন্দ্র", articles: [ {title: "গোবর গ্যাসের উপকারিতা", text: "গোবর গ্যাস জীবাশ্ম জ্বালানির ব্যবহার কমায় এবং মাটির স্বাস্থ্য উন্নত করে।", video: "https://www.youtube.com/embed/VIDEO_ID1"}, {title: "কম্পোস্টিং কৌশল", text: "ভাল ফলনের জন্য জৈব বর্জ্য কম্পোস্ট করার পদ্ধতি শিখুন।", video: "https://www.youtube.com/embed/VIDEO_ID2"}, {title: "জল সংরক্ষণ", text: "কৃষিতে জল সংরক্ষণের টিপস।", video: "" } ] },
      dashboard: { title: "ড্যাশবোর্ড", credits: "সবুজ ক্রেডিটস", weather: "আজকের আবহাওয়া" },
      successStories: [ {img: "assets/farmer1.jpg", quote: "গোবর গ্যাস আমার চাষ পরিবর্তন করেছে!", name: "রবি কুমার"}, {img: "assets/farmer2.jpg", quote: "এখন প্রতি মাসে LPG সাশ্রয় করি।", name: "লক্ষ্মী দেবী"}, {img: "assets/farmer3.jpg", quote: "স্লরি দিয়ে আমার ফসল আরও স্বাস্থ্যকর।", name: "মনোজ সিং" } ]
    }
  };

  // --- Utility: safe getElement ---
  function $id(id){ return document.getElementById(id); }

  // --- Page switcher ---
  function showPage(page){
    document.querySelectorAll('.page-section').forEach(sec => sec.style.display = 'none');
    const el = $id('page-' + page);
    if(el) el.style.display = '';
    currentPage = page;
    renderPage(currentPage);
  }

  // --- Speech helper ---
  function speak(text){
    if('speechSynthesis' in window && text){
      try{
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = currentLang === 'hi' ? 'hi-IN' : currentLang === 'ta' ? 'ta-IN' : currentLang === 'kn' ? 'kn-IN' : currentLang === 'bn' ? 'bn-IN' : 'en-US';
        window.speechSynthesis.speak(utter);
      }catch(e){ console.warn('TTS error', e); }
    }
  }

  // --- Renderers ---
  function renderHome(){
    const t = translations[currentLang].home;
    const container = $id('page-home');
    if(!container) return;
    container.innerHTML = `
      <section class="hero">
        <h1 class="hero-title">${t.heroTitle}</h1>
        <p class="hero-desc">${t.heroDesc}</p>
        <button class="cta-button" data-nav="about">${t.learnMore}</button>
      </section>
      <div class="video-section">
        <h3>${t.videoLabel}</h3>
        <iframe width="560" height="315" src="https://www.youtube.com/embed/5K7FhFz_xS4" frameborder="0" allowfullscreen></iframe>
      </div>
      <h2>${translations[currentLang].dashboard.title}</h2>
      <div class="dashboard-grid">
        <div class="card" tabindex="0">
          <h3>${translations[currentLang].dashboard.credits}</h3>
          <p class="credits-count" id="credits-count">${greenCredits}</p>
        </div>
        <div class="card" tabindex="0">
          <h3>${translations[currentLang].dashboard.weather}</h3>
          <p id="weather-info"></p>
        </div>
        <div class="card" tabindex="0">
          <h3>Daily Tip</h3>
          <p>${translations[currentLang].knowledge.articles[0].text}</p>
        </div>
      </div>
      <div class="carousel-section">
        <h2>Success Stories</h2>
        <div id="success-carousel"></div>
      </div>
    `;
    renderSuccessStories();
    renderWeather();
  }

  function renderDashboard(){
    const t = translations[currentLang].dashboard;
    const container = $id('page-dashboard');
    if(!container) return;
    container.innerHTML = `
      <h2>${t.title}</h2>
      <div class="dashboard-grid">
        <div class="card" tabindex="0">
          <h3>${t.credits}</h3>
          <p class="credits-count" id="credits-count">${greenCredits}</p>
        </div>
        <div class="card" tabindex="0">
          <h3>${t.weather}</h3>
          <p id="weather-info"></p>
        </div>
        <div class="card" tabindex="0">
          <h3>Daily Tip</h3>
          <p>${translations[currentLang].knowledge.articles[0].text}</p>
        </div>
      </div>
      <div class="carousel-section">
        <h2>Success Stories</h2>
        <div id="success-carousel"></div>
      </div>
    `;
    renderSuccessStories();
    renderWeather();
  }
  
  function renderCalculator() {
    const t = translations[currentLang].calc;
    const container = $id('page-calculator');
    if (!container) return;
    container.innerHTML = `
      <h2>${t.title}</h2>
      <form id="calc-form" autocomplete="off">
        <label for="waste-input">${t.label}</label>
        <input type="number" id="waste-input" min="0" step="1" required>
        <button type="submit">${t.btn}</button>
      </form>
      <div id="calc-result" class="output-card" tabindex="0" aria-live="polite"></div>
    `;
    const form = $id('calc-form');
    if (!form) return;
    form.onsubmit = function(e) {
      e.preventDefault();
      const wasteKg = Number($id('waste-input').value) || 0;
      const biogas = wasteKg * 0.04;
      const lpg = biogas * 2;
      const elec = biogas * 1.8;
      const co2 = biogas * 1.7;
      const results = [
        `${t.output[0]}: <b>${biogas.toFixed(2)}</b>`,
        `${t.output[1]}: <b>${lpg.toFixed(2)}</b>`,
        `${t.output[2]}: <b>${elec.toFixed(2)}</b>`,
        `${t.output[3]}: <b>${co2.toFixed(2)}</b>`
      ];
      const out = $id('calc-result');
      if(out) out.innerHTML = results.join('<br>');
      speak(results.map(r => r.replace(/<[^>]+>/g,'')).join('. '));
      greenCredits += 5;
      const cc = $id('credits-count'); if(cc) cc.textContent = greenCredits;
    };
  }


  
  function renderC2F(){
    const t = translations[currentLang].c2f;
    const container = $id('page-c2f');
    if(!container) return;
    container.innerHTML = `
      <h2>${t.title}</h2>
      <div style="margin-bottom:2em;background:#fffde7;padding:1em;border-radius:10px;box-shadow:0 2px 8px #fbc02d44;">
        <h3>How does the marketplace work?</h3>
        <ul style="font-size:1.1em;">
          <li>Restaurants/households post available wet waste</li>
          <li>Farmers/gas plants can claim waste for biogas production</li>
          <li>Claimed waste moves to a separate list</li>
        </ul>
      </div>
      <div id="c2f-available">
        <h3>${t.available}</h3>
        <div id="market-list"></div>
      </div>
      <div id="c2f-claimed">
        <h3>${t.claimed}</h3>
        <div id="claimed-list"></div>
      </div>
    `;
    renderMarketList();
    renderClaimedList();
  }

  function renderMarketList(){
    const tform = translations[currentLang].wetwaste.form;
    const tbtn = translations[currentLang].c2f.claimBtn;
    const list = $id('market-list');
    if(!list) return;
    if(marketEntries.length === 0){
      list.innerHTML = `<div style="color:#888;font-size:1.1em;">No entries yet.</div>`;
      return;
    }
    let html = `<table><tr><th>${tform[0]}</th><th>${tform[1]}</th><th>${tform[2]}</th><th>${tform[3]}</th><th></th></tr>`;
    marketEntries.forEach((entry, idx) =>{
      html += `<tr><td>${entry.name}</td><td>${entry.type}</td><td>${entry.quantity}</td><td>${entry.location}</td><td><button class="claim-btn" data-idx="${idx}" title="${tbtn}">${tbtn}</button></td></tr>`;
    });
    html += '</table>';
    list.innerHTML = html;

    list.querySelectorAll('.claim-btn').forEach(btn => {
      btn.onclick = function(){
        const idx = Number(this.getAttribute('data-idx'));
        if(isNaN(idx) || !marketEntries[idx]) return;
        claimedEntries.push(marketEntries[idx]);
        marketEntries.splice(idx,1);
        renderMarketList();
        renderClaimedList();
        greenCredits += 10;
        const cc = $id('credits-count'); if(cc) cc.textContent = greenCredits;
      };
    });
  }

  function renderClaimedList(){
    const tform = translations[currentLang].wetwaste.form;
    const list = $id('claimed-list');
    if(!list) return;
    if(claimedEntries.length === 0){
      list.innerHTML = `<div style="color:#888;font-size:1.1em;">No claimed entries yet.</div>`;
      return;
    }
    let html = `<table><tr><th>${tform[0]}</th><th>${tform[1]}</th><th>${tform[2]}</th><th>${tform[3]}</th></tr>`;
    claimedEntries.forEach(entry =>{
      html += `<tr class="claimed-row"><td>${entry.name}</td><td>${entry.type}</td><td>${entry.quantity}</td><td>${entry.location}</td></tr>`;
    });
    html += '</table>';
    list.innerHTML = html;
  }

  function renderWetWaste(){
    const t = translations[currentLang].wetwaste;
    const container = $id('page-wetwaste');
    if(!container) return;
    container.innerHTML = `
      <h2>${t.title}</h2>
      <div style="margin-bottom:2em;background:#fffde7;padding:1em;border-radius:10px;box-shadow:0 2px 8px #fbc02d44;">
        <h3>For Restaurants & Households</h3>
        <ul style="font-size:1.1em;">
          <li>Post your available wet waste for farmers to claim</li>
          <li>Help reduce landfill and support renewable energy</li>
        </ul>
      </div>
      <form id="wetwaste-form" autocomplete="off">
        <div class="form-row">
          <input type="text" id="ww-name" placeholder="${t.form[0]}" required>
          <select id="ww-type" required>
            ${t.types.map(type => `<option value="${type}">${type}</option>`).join('')}
          </select>
        </div>
        <div class="form-row">
          <input type="number" id="ww-qty" min="1" placeholder="${t.form[2]}" required>
          <input type="text" id="ww-loc" placeholder="${t.form[3]}" required>
        </div>
        <button type="submit" title="${t.form[4]}">${t.form[4]}</button>
      </form>
    `;

    const form = $id('wetwaste-form');
    if(!form) return;
    form.onsubmit = function(e){
      e.preventDefault();
      const name = ($id('ww-name')||{}).value?.trim();
      const type = ($id('ww-type')||{}).value;
      const quantity = Number(($id('ww-qty')||{}).value);
      const location = ($id('ww-loc')||{}).value?.trim();
      if(!name || !type || !quantity || !location) return;
      marketEntries.push({ name, type, quantity, location });
      // Re-render C2F to show new entry
      if(currentPage === 'c2f') renderC2F();
      form.reset();
      greenCredits += 7;
      const cc = $id('credits-count'); if(cc) cc.textContent = greenCredits;
    };
  }

  // --- Crop Guidance ---
  const cropData = [
    {crop: "Wheat", slurry: 1200, effluent: 400},
    {crop: "Rice", slurry: 1000, effluent: 350},
    {crop: "Sugarcane", slurry: 1500, effluent: 500},
    {crop: "Maize", slurry: 900, effluent: 300},
    {crop: "Vegetables", slurry: 800, effluent: 250}
  ];
  function renderCrop(){
    const t = translations[currentLang].crop;
    const container = $id('page-crop');
    if(!container) return;
    container.innerHTML = `
      <h2>${t.title}</h2>
      <div style="margin-bottom:2em;background:#fffde7;padding:1em;border-radius:10px;box-shadow:0 2px 8px #fbc02d44;">
        <h3>How to use Gobar Gas By-products?</h3>
        <ul style="font-size:1.1em;">
          <li>Slurry: Use as organic fertilizer for all major crops</li>
          <li>Liquid effluent: Use as bio-pesticide for vegetables and grains</li>
        </ul>
      </div>
      <table><tr>
        <th>${t.tableHead[0]}</th><th>${t.tableHead[1]}</th><th>${t.tableHead[2]}</th>
      </tr>
      ${cropData.map(row => `<tr><td>${row.crop}</td><td>${row.slurry}</td><td>${row.effluent}</td></tr>`).join('')}
      </table>
    `;
  }

  // --- Knowledge Hub ---
  function renderKnowledge(){
    const t = translations[currentLang].knowledge;
    const container = $id('page-knowledge');
    if(!container) return;
    container.innerHTML = `
      <h2>${t.title}</h2>
      <div style="margin-bottom:2em;background:#fffde7;padding:1em;border-radius:10px;box-shadow:0 2px 8px #fbc02d44;">
        <h3>Learn about:</h3>
        <ul style="font-size:1.1em;">
          <li>Gobar Gas Benefits</li>
          <li>Composting Techniques</li>
          <li>Water Conservation</li>
        </ul>
      </div>
      <div>
        ${t.articles.map(a => `
          <div class="card" style="margin-bottom:1em;">
            <h3>${a.title}</h3>
            <p>${a.text}</p>
            ${a.video ? `<iframe width="320" height="180" src="${a.video}" frameborder="0" allowfullscreen></iframe>` : ''}
          </div>
        `).join('')}
      </div>
    `;
    greenCredits += 3;
    const cc = $id('credits-count'); if(cc) cc.textContent = greenCredits;
  }

  // --- About & Contact ---
  function renderAbout(){
    const container = $id('page-about');
    if(!container) return;
    container.innerHTML = `
      <h2>About Us</h2>
      <div style="background:#fffde7;padding:1em;border-radius:10px;box-shadow:0 2px 8px #fbc02d44;max-width:600px;margin:auto;">
        <p>${translations[currentLang].about}</p>
        <ul style="font-size:1.1em;">
          <li>Farmer-first platform</li>
          <li>Supports sustainable agriculture</li>
          <li>Promotes renewable energy</li>
          <li>Connects farmers, restaurants, and experts</li>
        </ul>
      </div>
    `;
  }
  function renderContact(){
    const container = $id('page-contact');
    if(!container) return;
    container.innerHTML = `
      <h2>Contact Us</h2>
      <div style="background:#fffde7;padding:1em;border-radius:10px;box-shadow:0 2px 8px #fbc02d44;max-width:600px;margin:auto;">
        <p>${translations[currentLang].contact}</p>
        <ul style="font-size:1.1em;">
          <li>Email: support@agriai.com</li>
          <li>Phone: 1800-AGRI-AI</li>
          <li>Address: AgriAI+ HQ, India</li>
        </ul>
      </div>
    `;
  }

  // --- Weather (simple placeholder, replace with API call if desired) ---
  function renderWeather(){
    const info = $id('weather-info');
    if(!info) return;
    info.textContent = 'Sunny, 28°C';
  }

  // --- Success Stories carousel ---
  function renderSuccessStories(){
    const stories = translations[currentLang].successStories || [];
    const container = $id('success-carousel');
    if(!container) return;
    container.innerHTML = stories.map(s => `
      <div class="story-card" style="display:inline-block;margin:0 1em;text-align:center;max-width:160px">
        <img src="${s.img}" alt="${s.name}" style="width:120px;height:120px;border-radius:50%;object-fit:cover;">
        <blockquote style="font-size:0.9em;margin:0.5em 0;">"${s.quote}"</blockquote>
        <p style="margin:0;font-weight:bold;">${s.name}</p>
      </div>
    `).join('');
  }

  // --- Biogas Savings Calculator ---
  function renderBiogasSavings() {
    const t = translations[currentLang].biogasSavings;
    const container = $id('page-biogas-savings');
    if (!container) return;
    container.innerHTML = `
      <h2>${t.title}</h2>
      <form id="biogas-savings-form" autocomplete="off" style="margin-bottom:1em;">
        <label for="biogas-input">${t.biogasInput}</label>
        <input type="number" id="biogas-input" min="0" step="0.01" required>
        <label for="lpg-price-input">${t.lpgPriceInput}</label>
        <input type="number" id="lpg-price-input" min="1" step="1" value="100" required>
        <button type="submit">${t.btn}</button>
      </form>
      <div id="biogas-savings-result" class="output-card" tabindex="0" aria-live="polite"></div>
      <div style="margin-top:2em;background:#e8f5e9;padding:1em;border-radius:10px;box-shadow:0 2px 8px #388e3c22;">
        <h3>${t.howItWorks}</h3>
        <ul style="font-size:1.1em;">
          ${t.list.map(item => `<li>${item}</li>`).join('')}
        </ul>
      </div>
    `;
    const form = $id('biogas-savings-form');
    if (!form) return;
    form.onsubmit = function(e) {
      e.preventDefault();
      const biogas = Number($id('biogas-input').value) || 0;
      const lpgPrice = Number($id('lpg-price-input').value) || 100;
      const lpgEq = biogas * 0.43;
      const moneySaved = lpgEq * lpgPrice;
      const co2Saved = lpgEq * 2.9;
      const result = `
        <b>${t.resultDesc.money}:</b> ₹${moneySaved.toFixed(2)} 💰<br>
        <b>${t.resultDesc.co2}:</b> ${co2Saved.toFixed(2)} kg 🌱
      `;
      $id('biogas-savings-result').innerHTML = result;
      speak(`${t.resultDesc.money}: ₹${moneySaved.toFixed(2)}. ${t.resultDesc.co2}: ${co2Saved.toFixed(2)} kilograms.`);
      greenCredits += 8;
      const cc = $id('credits-count'); if(cc) cc.textContent = greenCredits;
    };
  }

  // --- Map pages to their render functions ---
  const pageRenderers = {
  'home': renderHome,
  'dashboard': renderDashboard,
  'calculator': renderCalculator,
  'biogas-savings': renderBiogasSavings,
  'c2f': renderC2F,
  'wetwaste': renderWetWaste,
  'crop': renderCrop,
  'knowledge': renderKnowledge,
  'about': renderAbout,
  'contact': renderContact
  };
  function renderPage(page){
    const renderFn = pageRenderers[page];
    if(renderFn) renderFn();
  }

  // --- Language setter (updates UI strings) ---
  function setLang(lang){
    if(!translations[lang]) return;
    currentLang = lang;
    const t = translations[lang];

    const navItems = document.querySelectorAll('#main-nav a');
    if (navItems) navItems.forEach((link, idx) => link.textContent = t.nav[idx]);

    const sidebarItems = document.querySelectorAll('.sidebar-menu .sidebar-btn');
if (sidebarItems) sidebarItems.forEach((btn, idx) => btn.textContent = t.sidebar[idx]);

    // Only re-render the current page after a language change
    renderPage(currentPage);
  }

  // --- Attach navigation handlers (guarded) ---
  function attachNavHandlers(){
    const maybe = (id, fn) => { const el = $id(id); if(el) el.onclick = fn; };
    maybe('nav-home', () => showPage('home'));
    maybe('nav-about', () => showPage('about'));
    maybe('nav-contact', () => showPage('contact'));

    maybe('menu-dashboard', () => showPage('dashboard'));
    maybe('menu-calculator', () => showPage('calculator'));
    maybe('menu-biogas-savings', () => showPage('biogas-savings'));
    maybe('menu-c2f', () => showPage('c2f'));
    maybe('menu-wetwaste', () => showPage('wetwaste'));
    maybe('menu-crop', () => showPage('crop'));
    maybe('menu-knowledge', () => showPage('knowledge'));

    document.querySelectorAll('[data-nav]').forEach(el => {
      el.addEventListener('click', function(){
        const target = this.getAttribute('data-nav'); if(target) showPage(target);
      });
    });
  }

  // --- Init when DOM ready ---
  document.addEventListener('DOMContentLoaded', function(){
    attachNavHandlers();
    
    const langSelect = $id('lang-select');
    if(langSelect){
      langSelect.value = currentLang;
      langSelect.addEventListener('change', function(){ setLang(this.value); });
    }

    setLang(currentLang);
    showPage('home');
  });

  // expose for debug (optional)
  window.AgriAI = {
    setLang: setLang,
    showPage: showPage,
    
    getState: () => ({ currentLang, currentPage, greenCredits, marketEntries, claimedEntries })
  };

})();