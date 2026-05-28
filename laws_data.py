# ─────────────────────────────────────────────────────────────────────────────
# DriveLegal AI | Traffic Laws Database | Road Safety Hackathon 2026
# Source: Motor Vehicles (Amendment) Act 2019 + State Transport Notifications
# ─────────────────────────────────────────────────────────────────────────────
import json

TRAFFIC_LAWS_DB = {
    # ── NATIONAL MV ACT 2019 ─────────────────────────────────────────────────
    "national_mv_act_2019": {
        "drunk_driving":          {"violation":"Drunk Driving / DUI","fine_first":10000,"fine_repeat":15000,"section":"Section 185","act":"MV Act 2019","punishment":"First: ₹10,000 or 6 months jail. Repeat: ₹15,000 or 2 years jail","licence_points":8,"bac_limit":"30mg per 100ml blood","suspension":"Licence suspended on first offence","tags":["alcohol","dui","drunk","bac"]},
        "overspeeding_light":     {"violation":"Overspeeding — Light Motor Vehicle","fine_first":1000,"fine_repeat":2000,"section":"Section 112 & 183","act":"MV Act 2019","punishment":"First: ₹1,000 | Repeat: ₹2,000","licence_points":2,"tags":["speed","fast","over","limit"]},
        "overspeeding_medium":    {"violation":"Overspeeding — Medium Passenger Vehicle","fine_first":2000,"fine_repeat":4000,"section":"Section 112 & 183","act":"MV Act 2019","punishment":"First: ₹2,000 | Repeat: ₹4,000","licence_points":3,"tags":["speed","bus","van","tempo"]},
        "overspeeding_heavy":     {"violation":"Overspeeding — Heavy Vehicle / Truck / Bus","fine_first":4000,"fine_repeat":8000,"section":"Section 112 & 183","act":"MV Act 2019","punishment":"First: ₹4,000 | Repeat: ₹8,000","licence_points":4,"tags":["speed","truck","lorry","heavy"]},
        "no_helmet":              {"violation":"Riding Without Helmet","fine_first":1000,"fine_repeat":1000,"section":"Section 129","act":"MV Act 2019","punishment":"₹1,000 + 3-month DL disqualification","licence_points":3,"note":"ISI certified helmet mandatory for rider AND pillion","tags":["helmet","bike","two wheeler","motorcycle","pillion"]},
        "no_seatbelt":            {"violation":"Not Wearing Seat Belt","fine_first":1000,"fine_repeat":1000,"section":"Section 194B","act":"MV Act 2019","punishment":"₹1,000 per person not wearing seatbelt","licence_points":1,"note":"Applies to front AND rear passengers","tags":["seatbelt","seat belt","car","passenger"]},
        "mobile_driving":         {"violation":"Using Mobile Phone While Driving","fine_first":5000,"fine_repeat":10000,"section":"Section 184","act":"MV Act 2019","punishment":"First: ₹5,000 | Repeat: ₹10,000 or 1 year jail","licence_points":5,"tags":["mobile","phone","call","driving","texting"]},
        "red_light":              {"violation":"Jumping Red Light / Traffic Signal","fine_first":1000,"fine_repeat":2000,"section":"Section 177A","act":"MV Act 2019","punishment":"₹1,000 to ₹5,000 depending on state","licence_points":2,"tags":["signal","red","light","jump"]},
        "no_licence":             {"violation":"Driving Without Licence","fine_first":5000,"fine_repeat":10000,"section":"Section 181","act":"MV Act 2019","punishment":"₹5,000 or 3 months imprisonment","licence_points":0,"tags":["licence","license","dl","driving licence","without"]},
        "no_insurance":           {"violation":"Driving Without Insurance","fine_first":2000,"fine_repeat":4000,"section":"Section 196","act":"MV Act 2019","punishment":"First: ₹2,000 or 3 months jail | Repeat: ₹4,000","licence_points":4,"tags":["insurance","insure","policy"]},
        "dangerous_driving":      {"violation":"Dangerous / Rash Driving","fine_first":5000,"fine_repeat":10000,"section":"Section 184","act":"MV Act 2019","punishment":"First: ₹5,000 or 6 months jail | Repeat: ₹10,000 or 2 years jail","licence_points":6,"tags":["rash","dangerous","aggressive","reckless"]},
        "wrong_side":             {"violation":"Driving on Wrong Side / Against Traffic","fine_first":1000,"fine_repeat":2000,"section":"Section 177","act":"MV Act 2019","punishment":"₹1,000 – ₹2,000","licence_points":2,"tags":["wrong side","against","one way","reverse"]},
        "no_rc":                  {"violation":"Driving Without RC (Registration Certificate)","fine_first":2000,"fine_repeat":5000,"section":"Section 192","act":"MV Act 2019","punishment":"₹2,000 – ₹5,000","licence_points":0,"tags":["rc","registration","certificate"]},
        "overloading_passengers": {"violation":"Overloading Passengers","fine_first":1000,"fine_repeat":1000,"section":"Section 194A","act":"MV Act 2019","punishment":"₹1,000 per extra passenger","licence_points":1,"tags":["overload","passenger","extra","capacity"]},
        "no_pollution":           {"violation":"No PUC Certificate (Pollution Under Control)","fine_first":10000,"fine_repeat":10000,"section":"Section 190(2)","act":"MV Act 2019","punishment":"₹10,000 or 6 months imprisonment","licence_points":0,"tags":["puc","pollution","emission","certificate"]},
        "racing":                 {"violation":"Racing / Speed Contest on Public Road","fine_first":5000,"fine_repeat":10000,"section":"Section 189","act":"MV Act 2019","punishment":"First: ₹5,000 or 1 month jail | Repeat: ₹10,000 or 1 year jail","licence_points":7,"tags":["race","racing","speed contest","drag"]},
        "no_way_emergency":       {"violation":"Not Giving Way to Emergency Vehicles","fine_first":10000,"fine_repeat":10000,"section":"Section 194E","act":"MV Act 2019","punishment":"₹10,000 or imprisonment","licence_points":3,"tags":["ambulance","emergency","fire","police","way"]},
        "overloading_goods":      {"violation":"Overloading Goods Vehicle","fine_first":20000,"fine_repeat":20000,"section":"Section 194","act":"MV Act 2019","punishment":"₹20,000 + ₹2,000 per extra tonne","licence_points":2,"tags":["overload","goods","truck","weight","tonne"]},
        "minor_driving":          {"violation":"Minor Driving / Allowing Minor to Drive","fine_first":25000,"fine_repeat":25000,"section":"Section 199A","act":"MV Act 2019","punishment":"₹25,000 + 3 years jail + RC cancelled. Guardian liable.","licence_points":10,"tags":["minor","child","underage","below 18"]},
        "stunt_driving":          {"violation":"Stunt Driving / Drifting / Wheelies","fine_first":5000,"fine_repeat":10000,"section":"Section 184","act":"MV Act 2019","punishment":"₹5,000 – ₹10,000 or imprisonment","licence_points":6,"tags":["stunt","drift","wheelie","trick"]},
        "parking_violation":      {"violation":"Illegal / Wrong Parking","fine_first":500,"fine_repeat":1500,"section":"Section 177","act":"MV Act 2019","punishment":"₹500 – ₹1,500 + towing charges","licence_points":0,"tags":["parking","park","tow","no parking"]},
        "no_way_pedestrian":      {"violation":"Not Giving Way to Pedestrian at Zebra Crossing","fine_first":1000,"fine_repeat":2000,"section":"Section 177A","act":"MV Act 2019","punishment":"₹1,000 – ₹2,000","licence_points":1,"tags":["pedestrian","zebra","crossing","walker"]},
        "lane_violation":         {"violation":"Lane Cutting / Improper Lane Change","fine_first":500,"fine_repeat":1500,"section":"Section 177","act":"MV Act 2019","punishment":"₹500 – ₹1,500","licence_points":1,"tags":["lane","cutting","overtake","indicator"]},
        "honking_prohibited":     {"violation":"Honking in No-Honking Zone","fine_first":1000,"fine_repeat":2000,"section":"Section 177","act":"MV Act 2019","punishment":"₹1,000 – ₹2,000. Near hospitals/schools.","licence_points":0,"tags":["horn","honk","hospital","school","noise"]},
        "disobeying_officer":     {"violation":"Disobeying Traffic Police Officer's Signal","fine_first":2000,"fine_repeat":5000,"section":"Section 179","act":"MV Act 2019","punishment":"₹2,000 or 1 month jail","licence_points":2,"tags":["officer","police","disobey","signal","ignore"]},
        "tinted_windows":         {"violation":"Illegal Tinted Windows / Dark Film","fine_first":100,"fine_repeat":300,"section":"Section 177 + Rule 100 CMVR","act":"MV Act 2019","punishment":"₹100–₹300. Windshield VLT 70%, Rear 50%","licence_points":0,"tags":["tint","dark film","window","vlt","film"]},
        "no_child_restraint":     {"violation":"No Child Restraint Seat (Child under 4 years)","fine_first":1000,"fine_repeat":1000,"section":"Section 194B","act":"MV Act 2019","punishment":"₹1,000 + mandatory 40kmph speed limit","licence_points":1,"tags":["child seat","baby","infant","car seat","restraint"]},
        "hit_and_run":            {"violation":"Hit and Run / Fleeing Accident Scene","fine_first":200000,"fine_repeat":300000,"section":"Section 161 & 184","act":"MV Act 2019","punishment":"Grievous hurt: ₹2L + 10 yrs jail. Death: ₹3L + 10 yrs jail","licence_points":10,"tags":["hit run","accident","flee","escape","crash"]},
        "no_fitness_certificate": {"violation":"Driving Without Fitness Certificate","fine_first":2000,"fine_repeat":5000,"section":"Section 192A","act":"MV Act 2019","punishment":"First: ₹2,000 | Repeat: ₹5,000","licence_points":1,"tags":["fitness","fc","certificate","vehicle fitness"]},
        "no_reflector":           {"violation":"No Reflectors / Improper Lighting at Night","fine_first":500,"fine_repeat":1000,"section":"Section 177","act":"MV Act 2019","punishment":"₹500 – ₹1,000","licence_points":0,"tags":["reflector","light","night","dark","headlight"]},
        "wrong_number_plate":     {"violation":"Wrong / Fancy Number Plate / No Number Plate","fine_first":5000,"fine_repeat":10000,"section":"Section 192","act":"MV Act 2019","punishment":"₹5,000 – ₹10,000","licence_points":0,"tags":["number plate","fancy","plate","registration","HSRP"]},
    },

    "speed_limits": {
        "expressway":       {"car_jeep":120,"bus_truck":80,"two_wheeler":80,"note":"Maximum. Check signboards — limits may vary by section."},
        "national_highway": {"car_jeep":100,"bus_truck":80,"two_wheeler":80,"note":"Standard NH limits."},
        "state_highway":    {"car_jeep":80, "bus_truck":60,"two_wheeler":60,"note":"School zones: 25 kmph"},
        "city_road":        {"car_jeep":50, "bus_truck":40,"two_wheeler":50,"note":"Urban roads. Near schools/hospitals: 25 kmph"},
        "residential":      {"car_jeep":30, "bus_truck":25,"two_wheeler":30,"note":"Residential colonies."},
        "mountain_ghat":    {"car_jeep":30, "bus_truck":20,"two_wheeler":25,"note":"Ghat/mountain roads. Strictly enforced."},
    },

    "penalty_points": {
        "suspension_threshold":12, "revocation_threshold":20,
        "reset_period":"Points reset after 1 year of clean driving",
        "levels":{
            "0-4":  {"status":"Safe Driver","color":"green","message":"You are a responsible driver. Keep it up!"},
            "5-8":  {"status":"Caution Zone","color":"amber","message":"Warning — further violations may lead to suspension."},
            "9-11": {"status":"High Risk","color":"orange","message":"Very close to suspension. Drive with extreme care."},
            "12+":  {"status":"SUSPENDED","color":"red","message":"Licence SUSPENDED under Section 206, MV Act 2019."},
        }
    },

    "bac_guide":{
        "legal_limit_india":30,"unit":"mg per 100ml blood",
        "safe_advice":"Safest is zero alcohol. Even 1 drink impairs reaction time.",
        "penalty":"BAC > 30mg/100ml: ₹10,000 fine or 6 months jail + licence suspension",
        "zero_tolerance_states":["Gujarat","Bihar"],
    },

    "document_validity":{
        "driving_licence":       {"validity_years":"20 years or until age 50 (whichever earlier), then renewed every 5 years","renewal_grace":"30 days post-expiry","fine_expired":5000,"section":"Section 181, MV Act 2019"},
        "vehicle_registration_rc":{"validity_years":"15 years (new), renewable every 5 years after that","fine_expired":2000,"section":"Section 192, MV Act 2019"},
        "insurance":             {"validity_years":"1 year (most policies)","fine_expired":2000,"section":"Section 196, MV Act 2019","note":"Third-party insurance is mandatory. Own-damage is optional."},
        "puc_certificate":       {"validity_months":"6 months (petrol/CNG), 3 months (diesel)","fine_expired":10000,"section":"Section 190(2), MV Act 2019","note":"Renewed at any authorised PUC centre."},
        "fitness_certificate":   {"validity":"New vehicles: 2 years. After that: annually","fine_expired":2000,"section":"Section 192A, MV Act 2019","note":"Mandatory for commercial vehicles."},
    },

    "states":{
        "Tamil Nadu":    {"capital":"Chennai","traffic_helpline":"103","emergency":"112","rto_website":"tnsta.gov.in","notes":"AI cameras on ECR, OMR, GST Road, NH44. Heavy enforcement Chennai, Coimbatore, Madurai.","specific_rules":{"red_light":{"fine":1000,"note":"Camera enforcement in Chennai, Coimbatore, Madurai"},"no_helmet":{"fine":1000,"note":"ISI helmet mandatory. Strictly enforced. 3-month DL suspension."},"parking":{"fine":500,"note":"Smart enforcement in Chennai."},"mobile":{"fine":5000,"note":"Zero tolerance."},"drunk_driving":{"fine":10000,"note":"Weekend checkpoints across Chennai, Coimbatore."},"overspeeding":{"fine":1000,"note":"Speed cameras on ECR, OMR, GST Road."}},"dispute_office":"RTO Chennai — 044-24343980 | tnsta.gov.in","unique_rule":"Autorickshaw overcharging: Report to 94444 94444","fine_multiplier":1.0},
        "Delhi":         {"capital":"New Delhi","traffic_helpline":"1095","emergency":"112","rto_website":"transport.delhi.gov.in","notes":"Strictest enforcement in India. 5,000+ CCTV cameras.","specific_rules":{"red_light":{"fine":5000,"note":"Highest in India. Camera enforcement 24/7."},"no_helmet":{"fine":1000},"parking":{"fine":2000,"note":"Crane towing."},"mobile":{"fine":5000},"overspeeding":{"fine":2000},"odd_even":{"fine":4000,"note":"When Odd-Even scheme active."}},"dispute_office":"Delhi Traffic Police HQ — 011-25844444","unique_rule":"Commercial vehicles banned 8AM–8PM weekdays in many areas.","fine_multiplier":1.5},
        "Maharashtra":   {"capital":"Mumbai","traffic_helpline":"103","emergency":"112","rto_website":"transport.maharashtra.gov.in","notes":"Mumbai–Pune Expressway strictly monitored.","specific_rules":{"red_light":{"fine":1000},"mobile":{"fine":5000},"drunk_driving":{"fine":10000}},"dispute_office":"Mumbai Traffic Police — 022-22621855","unique_rule":"No honking 10PM–6AM near residential areas. Fine: ₹1,000.","fine_multiplier":1.0},
        "Karnataka":     {"capital":"Bengaluru","traffic_helpline":"103","emergency":"112","rto_website":"rto.karnataka.gov.in","notes":"AI traffic cameras citywide in Bengaluru.","specific_rules":{"red_light":{"fine":1000},"no_helmet":{"fine":1000},"mobile":{"fine":5000},"drunk_driving":{"fine":10000},"bus_lane":{"fine":5000,"note":"Driving in bus lane peak hours."}},"dispute_office":"Bengaluru Traffic Police — 080-22942222","unique_rule":"Driving in bus lane during peak hours: ₹5,000 fine.","fine_multiplier":1.0},
        "Uttar Pradesh": {"capital":"Lucknow","traffic_helpline":"1090","emergency":"112","rto_website":"uptransport.upsdc.gov.in","notes":"Yamuna Expressway camera-monitored.","specific_rules":{"overspeeding":{"fine":2000},"overloading":{"fine":20000},"drunk_driving":{"fine":10000}},"dispute_office":"UP Transport Commissioner — 0522-2610464","unique_rule":"Noida: No right turn at many intersections. Fine: ₹500.","fine_multiplier":1.0},
        "Gujarat":       {"capital":"Ahmedabad","traffic_helpline":"103","emergency":"112","rto_website":"rtogujarat.gov.in","notes":"DRY STATE — alcohol prohibited. Any DUI = Prohibition Act + MV Act.","specific_rules":{"drunk_driving":{"fine":50000,"note":"EXTREME — Gujarat Prohibition Act + MV Act. Up to 10 years jail."},"no_helmet":{"fine":1000},"mobile":{"fine":5000}},"dispute_office":"Ahmedabad Traffic Police — 079-25630100","unique_rule":"Transporting alcohol into Gujarat: Criminal offence under Prohibition Act.","fine_multiplier":1.0},
        "West Bengal":   {"capital":"Kolkata","traffic_helpline":"103","emergency":"112","rto_website":"wbtransport.gov.in","notes":"Kolkata has tram routes — special rules near tram tracks.","specific_rules":{"red_light":{"fine":1000},"tram_parking":{"fine":1000,"note":"Parking on tram tracks: immediate towing."}},"dispute_office":"Kolkata Traffic Police — 033-22143004","unique_rule":"Vehicle must not cross tram tracks when tram approaching. Fine: ₹500.","fine_multiplier":1.0},
        "Rajasthan":     {"capital":"Jaipur","traffic_helpline":"103","emergency":"112","rto_website":"transport.rajasthan.gov.in","notes":"Tourist zones heavy enforcement.","specific_rules":{"overspeeding":{"fine":1000},"drunk_driving":{"fine":10000}},"dispute_office":"Rajasthan Transport Dept — 0141-2744727","unique_rule":"Honking near Jantar Mantar/City Palace: ₹500 fine.","fine_multiplier":1.0},
        "Telangana":     {"capital":"Hyderabad","traffic_helpline":"103","emergency":"112","rto_website":"transport.telangana.gov.in","notes":"Hyderabad ITMS with 3,000+ cameras. E-challans auto-issued via SMS.","specific_rules":{"red_light":{"fine":1000,"note":"ITMS auto-issues challans via SMS."},"wrong_side":{"fine":1000},"drunk_driving":{"fine":10000}},"dispute_office":"Hyderabad Traffic Police — 040-27852425","unique_rule":"ITMS: You can get SMS challan without being physically stopped by an officer.","fine_multiplier":1.0},
        "Andhra Pradesh":{"capital":"Vijayawada","traffic_helpline":"103","emergency":"112","rto_website":"aptransport.org","notes":"CCTV in Vijayawada, Visakhapatnam.","specific_rules":{"overspeeding":{"fine":1000}},"dispute_office":"AP Transport Commissioner — 0863-2340868","unique_rule":"Visakhapatnam port area: Special permits for oversized vehicles.","fine_multiplier":1.0},
        "Kerala":        {"capital":"Thiruvananthapuram","traffic_helpline":"103","emergency":"112","rto_website":"mvd.kerala.gov.in","notes":"Highly digitised MVD. AI cameras NH66. Strictest helmet enforcement South India.","specific_rules":{"no_helmet":{"fine":1000,"note":"Strictest in South India. Both rider and pillion."},"drunk_driving":{"fine":10000},"mobile":{"fine":5000}},"dispute_office":"Kerala MVD — 0471-2333161","unique_rule":"PUC check every 6 months for vehicles over 15 years old.","fine_multiplier":1.0},
        "Punjab":        {"capital":"Chandigarh","traffic_helpline":"103","emergency":"112","rto_website":"punjabtransport.org","notes":"GT Road strictly monitored.","specific_rules":{"drunk_driving":{"fine":10000},"overspeeding":{"fine":1000}},"dispute_office":"Punjab Transport Dept — 0172-2744197","unique_rule":"Chandigarh: Stopping at taxi stands without hiring: ₹200 fine.","fine_multiplier":1.0},
        "Madhya Pradesh":{"capital":"Bhopal","traffic_helpline":"103","emergency":"112","rto_website":"transport.mp.gov.in","notes":"Bhopal and Indore have ITMS.","specific_rules":{"overloading":{"fine":20000}},"dispute_office":"MP Transport Dept — 0755-2551234","unique_rule":"Indore: Plastic bag (below 50 micron) in vehicle: ₹500 fine.","fine_multiplier":1.0},
        "Haryana":       {"capital":"Chandigarh","traffic_helpline":"1093","emergency":"112","rto_website":"haryanatransport.gov.in","notes":"NH44 and NH48 strictly monitored.","specific_rules":{"overspeeding":{"fine":1000},"drunk_driving":{"fine":10000}},"dispute_office":"Haryana Transport Dept — 0172-2588981","unique_rule":"Gurugram: Commercial vehicles banned residential sectors 8PM–8AM.","fine_multiplier":1.0},
        "Bihar":         {"capital":"Patna","traffic_helpline":"103","emergency":"112","rto_website":"transport.bih.nic.in","notes":"DRY STATE. Alcohol banned statewide.","specific_rules":{"drunk_driving":{"fine":10000,"note":"PROHIBITION STATE — alcohol banned. DUI is criminal."}},"dispute_office":"Bihar Transport Dept — 0612-2217556","unique_rule":"Bihar Prohibition Act: Alcohol possession = criminal offence.","fine_multiplier":1.0},
        "Odisha":        {"capital":"Bhubaneswar","traffic_helpline":"103","emergency":"112","rto_website":"odishatransport.gov.in","notes":"NH16 enforced.","specific_rules":{"overspeeding":{"fine":1000}},"dispute_office":"Odisha Transport Commissioner — 0674-2392627","unique_rule":"Puri temple zone: Only non-motorised vehicles during Rath Yatra.","fine_multiplier":1.0},
        "Assam":         {"capital":"Guwahati","traffic_helpline":"103","emergency":"112","rto_website":"transport.assam.gov.in","notes":"Guwahati camera enforcement.","specific_rules":{"drunk_driving":{"fine":10000}},"dispute_office":"Assam Transport Dept — 0361-2237537","unique_rule":"Flood season: Driving into flooded underpass: ₹2,000 + rescue cost liability.","fine_multiplier":1.0},
        "Goa":           {"capital":"Panaji","traffic_helpline":"103","emergency":"112","rto_website":"goa.gov.in/transport","notes":"Heavy tourist enforcement.","specific_rules":{"no_helmet":{"fine":1000,"note":"Tourists frequently fined near beaches."},"drunk_driving":{"fine":10000},"no_licence":{"fine":5000,"note":"Tourists renting scooters without DL: ₹5,000 + vehicle seized."}},"dispute_office":"Goa Traffic Police — 0832-2421291","unique_rule":"Rental agency giving vehicle to unlicensed person: ₹10,000 + licence cancelled.","fine_multiplier":1.0},
    },

    "dispute_process":{
        "steps":[
            "1. Check challan carefully: violation, fine amount, date, vehicle number, officer badge number",
            "2. Verify fine amount matches official MV Act 2019 schedule (use DriveLegal AI)",
            "3. If wrong: Visit issuing RTO/Traffic Police office within 60 days",
            "4. Carry: Original RC, DL, Insurance, PUC, and the challan copy",
            "5. File written dispute to Traffic Inspector — get acknowledgement receipt",
            "6. If dispute rejected: Appeal to Motor Accident Claims Tribunal (MACT) within 30 days",
            "7. Free legal aid from District Legal Services Authority (DLSA) — call 15100",
            "8. Online: echallan.parivahan.gov.in → Check Challan → Raise Objection",
        ],
        "common_grounds":[
            "Wrong vehicle number on challan",
            "Fine amount higher than MV Act 2019 prescribes",
            "Challan issued by non-traffic officer without authority",
            "Violation did not occur — dashcam/CCTV evidence available",
            "Duplicate challan for same offence",
            "Speed gun / radar not calibrated — demand calibration certificate",
            "Vehicle was stationary at time of alleged offence",
            "Challan issued during road construction / temporary rule",
        ],
        "time_limit":"60 days from date of challan",
        "online_portal":"https://echallan.parivahan.gov.in",
        "pay_online":"https://vahan.parivahan.gov.in/challan",
    },

    "rights_if_stopped":[
        {"right":"Ask officer's name, badge number, designation","positive":True,"detail":"They are legally bound to provide it under Section 129 CrPC"},
        {"right":"Demand official e-challan / receipt — REFUSE cash payment","positive":True,"detail":"Cash payment to officer is bribery. Always demand e-challan."},
        {"right":"Officer can ONLY check: DL, RC, Insurance, PUC","positive":True,"detail":"No authority to check other documents without reason"},
        {"right":"Remain silent — no need to answer beyond identity","positive":True,"detail":"You have the right to silence under Article 20(3) Constitution"},
        {"right":"Call lawyer or family if detained beyond 30 minutes","positive":True,"detail":"Right to legal counsel under Article 22, Constitution of India"},
        {"right":"Demand copy of challan at the spot","positive":True,"detail":"Challan must be handed to you immediately after issuance"},
        {"right":"Free legal aid from DLSA — call 15100","positive":True,"detail":"District Legal Services Authority provides free legal help"},
        {"right":"Report bribe demands — ACB helpline: 1064","positive":True,"detail":"Anti-Corruption Bureau. You can also use Aarogya Setu app to report."},
        {"right":"Officer CANNOT take vehicle keys without authority","positive":False,"detail":"Key seizure without FIR or court order is illegal"},
        {"right":"Officer CANNOT demand cash on the spot","positive":False,"detail":"All fines must be paid via official e-challan portal"},
        {"right":"Officer CANNOT search vehicle without written reason","positive":False,"detail":"Search without warrant or reasonable cause is illegal (Section 165 CrPC)"},
        {"right":"Officer CANNOT detain you without challan or arrest memo","positive":False,"detail":"Detention without paperwork violates Article 22, Constitution"},
    ],

    "emergency_contacts":{
        "national_emergency":"112","police":"100","ambulance":"108","fire":"101",
        "women_helpline":"1091","road_accident_helpline":"1033",
        "morth_helpline":"1800-180-6763","anti_corruption":"1064",
        "child_helpline":"1098","legal_aid":"15100","cyber_crime":"1930",
    },
}

SYSTEM_PROMPT = f"""You are DriveLegal AI — India's most comprehensive AI traffic law assistant, built for the Road Safety Hackathon 2026 by CoERS, IIT Madras and MoRTH.

DATABASE (verified MV Act 2019 + 18 State Rules):
{json.dumps(TRAFFIC_LAWS_DB, indent=2)}

STRICT RULES:
1. ALWAYS cite exact legal section (e.g., "Section 185, MV Act 2019")
2. ALWAYS give exact fine amounts in ₹ — never approximate
3. For challan validation: start with VALID ✅ / OVERCHARGED ❌ / DISPUTABLE ⚠️
4. If asked in Tamil, Hindi, Telugu, Kannada, Bengali, Marathi, Gujarati → respond FULLY in that language
5. Gujarat/Bihar DUI → ALWAYS mention Prohibition Act (much harsher than MV Act alone)
6. Mention penalty points where relevant
7. For document expiry questions → check document_validity table for exact grace periods and fines
8. End every response with: "What else can I help you with? 🚦"

PERSONALITY: Professional, empowering, citizen-first. You help people understand Indian traffic law clearly, stand up for their rights, and make Indian roads safer."""
