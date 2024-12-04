from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from flask_cors import CORS
import time

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Retrieve API key from the environment variable
API_KEY = os.environ.get("GENAI_API_KEY")

# Configure the Generative AI model
genai.configure(api_key=API_KEY)
# Assuming you're using a fine-tuned model (real-estate-glossary-model in this case)
model = genai.GenerativeModel("gemini-1.5-flash")

# Define a route for the chatbot interaction
chat_history = [
    {"role": "user", "parts": "Hello, you are a chatbot designed to be a glossary for real estate. Only output in sentences."},
    {"role": "model", "parts": "Hello! How can I help you with real estate terms today?"}
]

glossary_terms = [
    "2-Way Lighting", "2-Wire Lighting System", "Abiotic components", "Abiotic depletion", "ACH (Air Changes per Hour)",
    "Acid rain", "Acidification", "Advanced Framing", "AECB", "Aerobic digestion", "Afforestation",
    "Air barrier / airtightness membrane", "Air film resistance", "Air infiltration", "Air leakage index",
    "Air permeability", "Air-Source Heat Pump", "Airtightness", "Airtightness layer", "Airtightness line",
    "Airtightness test", "Alexa", "Alexa Routine", "Alexa Skill", "Alpha - value", "Alternative energy", "Android",
    "Application Programming Interface (API)", "Automations", "Balance point", "Balancing pond", "Batt Insulation",
    "BFRC Rating", "Bio-accumulation", "Biocide", "Biodegradation", "Biofuel", "Biological wastewater treatment",
    "Biomass", "Bioretention area", "Bixby", "Blackwater", "Blower Door Test", "Blown-in Insulation", "Bluetooth",
    "Breathable sheathing", "Breather membrane", "Breathing wall", "BREEAM", "Bridge", "Brown roof", "Building Envelope",
    "CAPEM", "Carbon neutral", "Carbon sequestration", "Carbon sink", "CarbonLite Programme",
    "Chlorofluorocarbons (CFC)", "Closed Cell (spray) Foam Insulation (CCF)", "Closed loop-recycling", "Co-generation",
    "Code for Sustainable Homes", "Coefficient of performance (COP)", "Cold bridging", "Cold spot",
    "Combined Heat and Power (CHP)", "Communication Protocol", "Compost", "Composting toilet", "Conditioned Space",
    "Connected Device", "Connected Home", "Connectivity Session", "Control4", "Cortana", "Cradle-to-*",
    "Cross-laminated timber (CLT) panels", "Daylight transmittance", "Deconstruction", "Decrement delay",
    "Decrement factor", "Deforestation", "Degree days", "Delivered energy", "Desertification",
    "Design for Deconstruction (DfD)", "Diffuse pollution", "Diffusion Open", "Diffusion Tight", "Direct-Gain System",
    "Displacement Ventilation", "Distributed generation", "District heating", "Diurnal heat flow",
    "Diurnal temperature variation", "Double Pane Windows", "Double-Stud Wall", "Downcycle", "Drainage Plane", "Driver",
    "Dual-Mesh Network", "Dynamic Pricing", "Earth construction", "Eco Sinope", "Eco-design", "Eco-label",
    "Effective Leakage Area", "Embodied energy", "Energy Assessment", "Energy Consumption Graphs", "Energy efficiency",
    "Engineered wood", "Energy Recovery Ventilator", "Energy Truss", "Engineered Lumber", "Enhanced Air Filtration",
    "Environmental profile", "Environmental profiling", "Ethernet", "Eutrophication", "Evaporative cooling", "Event",
    "f-factor", "Fan Pressurisation Test", "Filter drain", "Filtration", "Flood routeing", "Flow control device",
    "Fly ash (PFA - Pulverised Fuel Ash)", "Fossil fuel", "Framing", "Fresh water aquatic ecotoxicity", "G-value",
    "Gasification", "Gateway", "Geofencing", "Geolocation", "Geotextile", "Geothermal energy",
    "Global Warming Potential (GWP)", "Google Assistant", "Google Home", "Green Building Standards", "Green Electricity",
    "Green Guide to Specification", "Green Power", "Green Register", "Green roof", "Greenhouse gases", "Greenwash",
    "Greywater", "Greywater Reuse", "Ground source heat pump (GSHP)", "Groundwater", "Hazardous waste", "Heat capacity",
    "Heat exchanger", "Heat island", "Heat Loss Parameter (HLP)", "Heat Pump", "Heat recovery",
    "Heat Recovery Ventilator", "Hot spots", "Home Automation", "Home Energy Rating System", "Home ID", "HomeKit", "Hub",
    "Hubitat", "Human toxicity", "Humidity", "Hydrocarbons", "Hydrochlorofluorocarbon (HCFC)", "Hydrofluorocarbon (HFC)",
    "Hygroscopic material", "Ice Dam", "Impermeable surface", "Indoor air quality (IAQ)", "Insulated Concrete Form",
    "Insulated Glass", "Insulating concrete formwork (ICF)", "Intelligent building", "Insulation", "Integration",
    "Internal heat gains", "Internet of Things (IoT)", "Interstitial condensation", "K-value", "Kiosk", "Land use",
    "Life cycle assessment (LCA)", "Life cycle costing (LCC)", "Life cycle approach", "Light pollution",
    "Living Building", "Low-Emissivity (Low-E) glass", "Low-impact development (LID)", "Low-Voltage lighting",
    "MERV rating", "Microgrid", "Microplastics", "Modular construction", "Modular Home", "Net-Zero Energy Building",
    "Non-Renewable energy", "Offsetting", "Onsite renewable energy", "Open-loop geothermal", "Passive house",
    "Passive Solar Design", "Photovoltaic (PV) energy", "Pollinator-friendly design", "Pollutant", "Pre-Assessment",
    "Prescriptive approach", "Proximity sensor", "Rain garden", "Renewable energy", "Retrofitting", "Roof garden",
    "Roof overhang", "Runoff", "Sanitary landfill", "Scaffolding", "Smart Building Technology", "Smart Grid",
    "Smart Meter", "Solar thermal energy", "Solar shading", "Solar tracker", "Solar wall", "Sustainable Architecture",
    "Sustainable Development", "Sustainable Materials", "Smart Building", "Smart Home", "Smart HVAC system",
    "Smart thermostat", "Solar panel", "Solar water heater", "Stormwater management", "Sustainable Urban Development",
    "Sustainability report", "Sustainable design", "Thermal bridge", "Thermal envelope", "Thermal mass",
    "Thermal transmittance", "Urban heat island", "Urban Planning", "Ventilation", "Vertical garden",
    "Water-efficient landscaping", "Water Harvesting", "Water Recycling", "Waterway", "Wetland", "Wind turbine",
    "Zero-energy building", "Zoning"
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/definition/<term>', methods=['GET'])
def get_definition(term):
    
    user_question = f"Define the term '{term}' in simple language. Please respond in no more than 100 words so that the user can understand. These are terms related to sustainabilty living."

    # Append the user's question to the chat history for context
    chat_history.append({"role": "user", "parts": user_question})

    try:
        # Create a new chat session with the model, using the updated chat history
        chat_session = model.start_chat(history=chat_history)

        # Send the term definition request to the model
        response = chat_session.send_message(user_question)

        # Extract the response text
        response_text = response.text if hasattr(response, 'text') else "No response available."
        
    except Exception as e:
        print("Error calling chat model:", str(e))
        return jsonify({"error": "Failed to communicate with the model."}), 500

    # Append the model's response to the chat history
    chat_history.append({"role": "model", "parts": response_text})

    return jsonify({"term": term, "definition": response_text})

@app.route('/api/glossary', methods=['GET'])
def get_glossary():
    
    # Return the complete glossary terms list sorted alphabetically.
   
    return jsonify(sorted(glossary_terms))
    
@app.route('/api/search', methods=['GET'])
def search_glossary():
    query = request.args.get('query', '').lower()

    if query:
        # Filter terms that start with the query
        filtered_terms = [term for term in glossary_terms if term.lower().startswith(query)]
        filtered_terms.sort()  # Sort terms alphabetically
    else:
        filtered_terms = glossary_terms

    return jsonify(filtered_terms)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
