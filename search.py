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
#model = genai.GenerativeModel("gemini-1.5-flash")
model = genai.GenerativeModel("tunedModels/real-estate-glossary-model-ug8dc3qfiqjf")

# Define a route for the chatbot interaction
# Store the chat history in a global variable
chat_history = [
    {"role": "user", "parts": "Hello, you are a chatbot designed to be a glossary for real estate. Only output in sentences."},
    {"role": "model", "parts": "Hello! How can I help you with real estate terms today?"}  # Shortened response
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat_with_bot():
    global chat_history
    data = request.get_json()
    user_question = data.get('question')+ "Please respond in no more than 100 words so that the user can understand"

    if not user_question:
        return jsonify({"error": "Question is required"}), 400
    

    # Append the user's question to the chat history
    chat_history.append({"role": "user", "parts": user_question})

    try:
        # Create a new chat session
        chat_session = model.start_chat(history=chat_history)

        # Generate a response from the model using send_message
        response = chat_session.send_message(user_question)
    except Exception as e:
        print("Error calling chat model:", str(e))
        return jsonify({"error": "Failed to communicate with the model."}), 500

    
    response_text = response.text if hasattr(response, 'text') else "No response text available"



    # Append the model's response to the chat history
    chat_history.append({"role": "model", "parts": response_text})

    return jsonify({"response": response_text})

@app.route('/api/fine-tune', methods=['POST'])
def fine_tune_model():
    # Define the training data
    training_data = [
    {"text_input": "What is 2-Way Lighting?", "output": "2-Way Lighting refers to a lighting system that allows control from two different switches, typically used in hallways or staircases to improve convenience and safety."},
    {"text_input": "What is a 2-Wire Lighting System?", "output": "A 2-Wire Lighting System is an electrical setup where both the power and control signals share the same two wires, often used in simpler lighting configurations."},
    {"text_input": "What are abiotic components?", "output": "Abiotic components are the non-living chemical and physical parts of the environment that affect living organisms and the functioning of ecosystems, such as water, air, and minerals."},
    {"text_input": "What is abiotic depletion?", "output": "Abiotic depletion refers to the reduction in non-renewable resources such as fossil fuels and minerals due to human consumption and extraction."},
    {"text_input": "What does ACH (Air Changes per Hour) mean?", "output": "ACH (Air Changes per Hour) is a measure of how many times the air within a defined space is replaced with outside air in one hour, important for assessing ventilation efficiency."},
    {"text_input": "What is acid rain?", "output": "Acid rain is precipitation that is significantly more acidic than normal, caused by the release of sulfur dioxide and nitrogen oxides into the atmosphere, which then react with water vapor."},
    {"text_input": "What is acidification?", "output": "Acidification refers to the process of increasing the acidity of an environment, typically water bodies, due to the absorption of atmospheric carbon dioxide or acid rain."},
    {"text_input": "What is Advanced Framing?", "output": "Advanced Framing is a construction technique that optimizes the use of materials and improves energy efficiency by reducing thermal bridging and minimizing waste."},
    {"text_input": "What is AECB?", "output": "AECB stands for the Association for Environment Conscious Building, a UK-based organization focused on sustainable building practices and improving the environmental impact of buildings."},
    {"text_input": "What is aerobic digestion?", "output": "Aerobic digestion is a biological process that breaks down organic matter in the presence of oxygen, often used in wastewater treatment to reduce sludge volume and organic content."},
    {"text_input": "What is afforestation?", "output": "Afforestation is the process of planting trees in an area where there was no previous tree cover, aimed at restoring ecosystems, enhancing biodiversity, and combating climate change."},
    {"text_input": "What is an air barrier / airtightness membrane?", "output": "An air barrier or airtightness membrane is a material used in building construction to prevent the flow of air between the interior and exterior of a building, improving energy efficiency."},
    {"text_input": "What is air film resistance?", "output": "Air film resistance is the resistance to heat transfer due to the thin layer of still air adjacent to a surface, contributing to overall thermal resistance in building components."},
    {"text_input": "What is air infiltration?", "output": "Air infiltration is the unintentional or accidental introduction of outside air into a building, often through cracks and openings, which can affect energy efficiency and indoor air quality."},
    {"text_input": "What is the air leakage index?", "output": "The air leakage index is a metric used to quantify the amount of air that leaks from a building, typically measured in cubic feet per minute per square foot of building area."},
    {"text_input": "What is air permeability?", "output": "Air permeability is the measure of how easily air can pass through a building material, affecting the energy efficiency and indoor air quality of structures."},
    {"text_input": "What is an Air-Source Heat Pump?", "output": "An Air-Source Heat Pump is a heating and cooling system that transfers heat to and from the outside air, providing efficient temperature regulation for buildings."},
    {"text_input": "What is airtightness?", "output": "Airtightness refers to the quality of a building's envelope that prevents uncontrolled air leakage, essential for maintaining energy efficiency and indoor air quality."},
    {"text_input": "What is an airtightness layer?", "output": "An airtightness layer is a barrier or membrane within a building's construction that minimizes air leakage, contributing to the overall energy efficiency of the building."},
    {"text_input": "What is an airtightness line?", "output": "An airtightness line is a specified path in building construction that indicates where airtightness measures should be applied to prevent air leakage."},
    {"text_input": "What is an airtightness test?", "output": "An airtightness test measures the air leakage of a building, typically using a blower door test to assess how well a building envelope prevents uncontrolled air flow."},
    {"text_input": "What is Alexa?", "output": "Alexa is a virtual assistant developed by Amazon, designed to perform tasks and provide information through voice commands using compatible devices."},
    {"text_input": "What is an Alexa Routine?", "output": "An Alexa Routine is a feature that allows users to automate multiple actions with a single voice command, such as turning on lights, adjusting thermostats, and playing music."},
    {"text_input": "What is an Alexa Skill?", "output": "An Alexa Skill is a third-party application that enhances the functionality of Alexa, allowing users to access additional features, services, and information."},
    {"text_input": "What is Alpha - value?", "output": "The Alpha value is a measure of the thermal transmittance of a material or construction element, indicating its effectiveness in insulating against heat loss."},
    {"text_input": "What is alternative energy?", "output": "Alternative energy refers to energy sources that are not based on fossil fuels, including renewable resources like solar, wind, hydro, and geothermal energy."},
    {"text_input": "What is Android?", "output": "Android is an open-source operating system developed by Google for mobile devices, such as smartphones and tablets, based on the Linux kernel."},
    {"text_input": "What is an Application Programming Interface (API)?", "output": "An Application Programming Interface (API) is a set of rules and protocols that allow different software applications to communicate and interact with each other."},
    {"text_input": "What are automations?", "output": "Automations refer to the use of technology to perform tasks with minimal human intervention, often applied in smart homes and business processes to increase efficiency."},
    {"text_input": "What is a Balance point?", "output": "The Balance point is the temperature at which a building does not require heating or cooling, as the internal heat gain equals the heat loss."},
    {"text_input": "What is a Balancing pond?", "output": "A Balancing pond is a water management feature that temporarily stores runoff water to manage flow rates and prevent flooding."},
    {"text_input": "What is Batt Insulation?", "output": "Batt Insulation is a type of insulation made of fiberglass or mineral wool, typically pre-cut into batts or rolls for easy installation between studs and joists."},
    {"text_input": "What is a BFRC Rating?", "output": "The BFRC Rating is an energy efficiency rating system for windows and doors in the UK, indicating their thermal performance."},
    {"text_input": "What is Bio-accumulation?", "output": "Bio-accumulation refers to the gradual accumulation of substances, such as pesticides or heavy metals, in an organism over time."},
    {"text_input": "What is a Biocide?", "output": "A Biocide is a chemical substance that can kill living organisms, often used for pest control and in various industrial applications."},
    {"text_input": "What is Biodegradation?", "output": "Biodegradation is the process by which organic substances are broken down by living organisms, typically bacteria, into simpler, non-toxic substances."},
    {"text_input": "What is Biofuel?", "output": "Biofuel is a type of renewable energy derived from biological materials, such as plants or animal waste, used as an alternative to fossil fuels."},
    {"text_input": "What is Biological wastewater treatment?", "output": "Biological wastewater treatment is a process that uses microorganisms to break down organic matter in wastewater."},
    {"text_input": "What is Biomass?", "output": "Biomass refers to organic materials used as a source of energy, which can be derived from plants, agricultural residues, and animal waste."},
    {"text_input": "What is a Bioretention area?", "output": "A Bioretention area is a landscaped area designed to manage stormwater runoff by using soil and vegetation to filter and absorb water."},
    {"text_input": "What is Bixby?", "output": "Bixby is a virtual assistant developed by Samsung, integrated into its devices to perform tasks and provide information."},
    {"text_input": "What is Blackwater?", "output": "Blackwater is wastewater that contains human waste and is typically generated from toilets, requiring special treatment."},
    {"text_input": "What is a Blower Door Test?", "output": "A Blower Door Test is a diagnostic tool used to measure the airtightness of a building by creating a pressure difference."},
    {"text_input": "What is Blown-in Insulation?", "output": "Blown-in Insulation is a type of insulation made from loose materials that are blown into walls and attics for improved thermal performance."},
    {"text_input": "What is Bluetooth?", "output": "Bluetooth is a wireless technology standard for short-range communication between devices, such as smartphones and headphones."},
    {"text_input": "What is Breathable sheathing?", "output": "Breathable sheathing is a type of building material that allows moisture vapor to escape while preventing liquid water from entering."},
    {"text_input": "What is a Breather membrane?", "output": "A Breather membrane is a material used in construction that allows water vapor to escape while providing a barrier to liquid water."},
    {"text_input": "What is a Breathing wall?", "output": "A Breathing wall is a wall system designed to manage moisture, allowing air and vapor to move through the wall assembly."},
    {"text_input": "What is BREEAM?", "output": "BREEAM (Building Research Establishment Environmental Assessment Method) is an environmental assessment method for master planning projects and buildings."},
    {"text_input": "What is a Bridge?", "output": "In construction, a bridge refers to a structure built to span physical obstacles, such as bodies of water or roads, allowing passage."},
    {"text_input": "What is a Brown roof?", "output": "A Brown roof is a type of green roof designed to promote biodiversity by allowing vegetation and wildlife to thrive."},
    {"text_input": "What is the Building Envelope?", "output": "The Building Envelope is the physical separator between the interior and exterior environments of a building, including walls, roofs, and foundations."},
    {"text_input": "What is CAPEM?", "output": "CAPEM stands for Carbon Accounting for Energy Management, a framework for measuring and managing energy-related carbon emissions."},
    {"text_input": "What does Carbon neutral mean?", "output": "Carbon neutral refers to achieving a balance between emitting carbon and absorbing carbon from the atmosphere, often achieved through offsets."},
    {"text_input": "What is Carbon sequestration?", "output": "Carbon sequestration is the process of capturing and storing atmospheric carbon dioxide to mitigate climate change."},
    {"text_input": "What is a Carbon sink?", "output": "A Carbon sink is a natural or artificial reservoir that absorbs and stores carbon dioxide from the atmosphere."},
    {"text_input": "What is the CarbonLite Programme?", "output": "The CarbonLite Programme is an initiative aimed at reducing carbon footprints in the construction industry through innovative practices."},
    {"text_input": "What are Chlorofluorocarbons (CFC)?", "output": "Chlorofluorocarbons (CFC) are chemical compounds used in refrigeration and aerosol propellants, known to deplete the ozone layer."},
    {"text_input": "What is Closed Cell (spray) Foam Insulation (CCF)?", "output": "Closed Cell Foam Insulation is a type of spray foam insulation that is dense and has a low permeability to air and moisture."},
    {"text_input": "What is Closed loop-recycling?", "output": "Closed loop-recycling refers to the process of recycling materials back into the same product, reducing waste and resource consumption."},
    {"text_input": "What is Co-generation?", "output": "Co-generation is the simultaneous production of electricity and useful heat from the same energy source."},
    {"text_input": "What is the Code for Sustainable Homes?", "output": "The Code for Sustainable Homes is a national standard in the UK for the sustainable design and construction of new homes."},
    {"text_input": "What is the Coefficient of performance (COP)?", "output": "The Coefficient of performance (COP) is a ratio that measures the efficiency of heating and cooling systems."},
    {"text_input": "What is Cold bridging?", "output": "Cold bridging occurs when heat is conducted through a material that has a higher thermal conductivity than surrounding materials."},
    {"text_input": "What is a Cold spot?", "output": "A Cold spot is an area in a building that is significantly cooler than surrounding areas, often due to insulation issues."},
    {"text_input": "What is Combined Heat and Power (CHP)?", "output": "Combined Heat and Power (CHP) is a technology that generates electricity and useful heat simultaneously from the same energy source."},
    {"text_input": "What is a Communication Protocol?", "output": "A Communication Protocol is a set of rules governing the exchange of data between devices in a network."},
    {"text_input": "What is Compost?", "output": "Compost is organic matter that has been decomposed and recycled as a fertilizer for soil."},
    {"text_input": "What is a Composting toilet?", "output": "A Composting toilet is a type of toilet that treats human waste by composting it into usable organic material."},
    {"text_input": "What is a Conditioned Space?", "output": "A Conditioned Space is an area in a building that is heated and cooled to maintain comfort levels."},
    {"text_input": "What is a Connected Device?", "output": "A Connected Device is an electronic device that can connect to the internet and communicate with other devices."},
    {"text_input": "What is a Connected Home?", "output": "A Connected Home is a residence equipped with smart devices that can be controlled remotely or automated."},
    {"text_input": "What is a Connectivity Session?", "output": "A Connectivity Session is a period during which devices are connected to a network for data transmission."},
    {"text_input": "What is Control4?", "output": "Control4 is a home automation company that provides technology solutions to manage smart home systems."},
    {"text_input": "What is Cortana?", "output": "Cortana is a virtual assistant created by Microsoft that uses AI to provide assistance and perform tasks."},
    {"text_input": "What is Cradle-to-*?", "output": "Cradle-to-* refers to a life cycle approach to product design and manufacturing, considering the entire life span of a product."},
    {"text_input": "What are Cross-laminated timber (CLT) panels?", "output": "Cross-laminated timber (CLT) panels are engineered wood products made from layers of timber glued together, providing strength and stability."},
    {"text_input": "What is Daylight transmittance?", "output": "Daylight transmittance measures the amount of daylight that passes through a glazing material."},
    {"text_input": "What is Deconstruction?", "output": "Deconstruction is the process of carefully dismantling buildings for reuse and recycling of materials."},
    {"text_input": "What is Decrement delay?", "output": "Decrement delay refers to the time it takes for a building's temperature to change in response to external temperature fluctuations."},
    {"text_input": "What is a Decrement factor?", "output": "The Decrement factor measures the reduction in temperature variation within a building's thermal mass."},
    {"text_input": "What is Deforestation?", "output": "Deforestation is the large-scale removal of trees from forests or land for agricultural or urban development."},
    {"text_input": "What are Degree days?", "output": "Degree days are a measure of heating or cooling needs based on temperature deviations from a standard."},
    {"text_input": "What is Delivered energy?", "output": "Delivered energy is the total energy provided to a building, including all forms of energy used."},
    {"text_input": "What is Desertification?", "output": "Desertification is the process by which fertile land becomes increasingly arid and unproductive, often due to human activity."},
    {"text_input": "What is Design for Deconstruction (DfD)?", "output": "Design for Deconstruction (DfD) is an approach to building design that facilitates easy disassembly and material reuse."},
    {"text_input": "What is Diffuse pollution?", "output": "Diffuse pollution refers to pollution that comes from multiple, often indistinct sources, making it difficult to identify specific contributors."},
    {"text_input": "What is Diffusion Open?", "output": "Diffusion Open refers to a material or system that allows moisture to move freely through it."},
    {"text_input": "What is Diffusion Tight?", "output": "Diffusion Tight refers to materials that restrict the movement of moisture vapor, often used in building envelopes."},
    {"text_input": "What is a Direct-Gain System?", "output": "A Direct-Gain System is a passive solar design approach that captures and utilizes solar energy for heating directly within living spaces."},
    {"text_input": "What is Displacement Ventilation?", "output": "Displacement Ventilation is a method of providing fresh air to a space through low-velocity airflow from the floor."},
    {"text_input": "What is Distributed generation?", "output": "Distributed generation refers to decentralized energy production systems, such as rooftop solar panels."},
    {"text_input": "What is District heating?", "output": "District heating is a system for distributing heat generated in a central location for residential and commercial heating."},
    {"text_input": "What is Diurnal heat flow?", "output": "Diurnal heat flow refers to the daily variation in heat movement through building materials due to temperature changes."},
    {"text_input": "What is Diurnal temperature variation?", "output": "Diurnal temperature variation refers to the change in temperature that occurs throughout the day."},
    {"text_input": "What are Double Pane Windows?", "output": "Double Pane Windows are windows made with two panes of glass, providing better insulation than single-pane windows."},
    {"text_input": "What is a Double-Stud Wall?", "output": "A Double-Stud Wall is a wall assembly that uses two sets of studs to increase insulation and reduce thermal bridging."},
    {"text_input": "What is Downcycle?", "output": "Downcycle refers to the recycling process where materials are converted into lower quality products."},
    {"text_input": "What is a Drainage Plane?", "output": "A Drainage Plane is a layer in a building assembly that facilitates the movement of water away from sensitive areas."},
    {"text_input": "What is a Driver?", "output": "In building technology, a Driver refers to a component that controls the operation of devices within a system."},
    {"text_input": "What is a Dual-Mesh Network?", "output": "A Dual-Mesh Network is a network topology that uses two overlapping mesh networks for improved connectivity."},
    {"text_input": "What is Dynamic Pricing?", "output": "Dynamic Pricing is a pricing strategy where prices fluctuate based on market demand and supply."},
    {"text_input": "What is Earth construction?", "output": "Earth construction involves building with natural materials, such as clay and earth, for sustainable structures."},
    {"text_input": "What is Eco Sinope?", "output": "Eco Sinope refers to sustainable practices and innovations that minimize environmental impact."},
    {"text_input": "What is Eco-design?", "output": "Eco-design is the process of designing products with consideration for their environmental impact throughout their life cycle."},
    {"text_input": "What is an Eco-label?", "output": "An Eco-label is a certification indicating that a product meets specific environmental standards."},
    {"text_input": "What is Effective Leakage Area?", "output": "Effective Leakage Area refers to the area through which air can leak from a building, affecting energy efficiency."},
    {"text_input": "What is Embodied energy?", "output": "Embodied energy is the total energy required to produce a building material, including extraction, processing, and transportation."},
    {"text_input": "What is an Energy Assessment?", "output": "An Energy Assessment is an evaluation of a building's energy use and efficiency, often leading to recommendations for improvements."},
    {"text_input": "What are Energy Consumption Graphs?", "output": "Energy Consumption Graphs visually represent a building's energy usage over time, helping to identify trends and inefficiencies."},
    {"text_input": "What is Energy efficiency?", "output": "Energy efficiency refers to using less energy to achieve the same level of performance or comfort."},
    {"text_input": "What is Engineered wood?", "output": "Engineered wood is a man-made wood product made from various wood materials bonded together, often stronger than solid wood."},
    {"text_input": "What is an Energy Recovery Ventilator?", "output": "An Energy Recovery Ventilator (ERV) is a system that exchanges stale indoor air with fresh outdoor air while recovering heat."},
    {"text_input": "What is an Energy Truss?", "output": "An Energy Truss is a structural framework designed to optimize energy efficiency in a building's design."},
    {"text_input": "What is Engineered Lumber?", "output": "Engineered Lumber refers to composite wood products manufactured for greater strength and stability compared to traditional lumber."},
    {"text_input": "What is Enhanced Air Filtration?", "output": "Enhanced Air Filtration refers to improved systems designed to remove contaminants from indoor air more effectively."},
    {"text_input": "What is an Environmental profile?", "output": "An Environmental profile outlines a product's environmental impacts throughout its life cycle."},
    {"text_input": "What is Environmental profiling?", "output": "Environmental profiling is the assessment of a product's environmental performance compared to alternatives."},
    {"text_input": "What is Ethernet?", "output": "Ethernet is a technology for connecting computers and devices in a local area network (LAN) using cables."},
    {"text_input": "What is Eutrophication?", "output": "Eutrophication is the process by which water bodies become overly enriched with nutrients, leading to excessive growth of algae."},
    {"text_input": "What is Evaporative cooling?", "output": "Evaporative cooling is a natural cooling process that uses water evaporation to cool the air."},
    {"text_input": "What is an Event?", "output": "In technology, an Event refers to an action or occurrence detected by a system that may require a response."},
    {"text_input": "What is the f-factor?", "output": "The f-factor is a measurement used in building energy calculations to account for factors affecting energy performance."},
    {"text_input": "What is a Fan Pressurisation Test?", "output": "A Fan Pressurisation Test measures a building's airtightness by using a fan to create a pressure difference."},
    {"text_input": "What is a Filter drain?", "output": "A Filter drain is a drainage system that allows water to pass through a porous material while filtering out sediment."},
    {"text_input": "What is Filtration?", "output": "Filtration is the process of separating solids from liquids or gases using a filter medium."},
    {"text_input": "What is Flood routeing?", "output": "Flood routeing is the process of managing and directing floodwaters to minimize damage."},
    {"text_input": "What is a Flow control device?", "output": "A Flow control device regulates the flow of fluids in a system to ensure optimal operation."},
    {"text_input": "What is Fly ash (PFA - Pulverised Fuel Ash)?", "output": "Fly ash is a byproduct from burning pulverised coal in electric power generating plants, used as a lightweight construction material."},
    {"text_input": "What is Fossil fuel?", "output": "Fossil fuel is a natural fuel formed from the remains of ancient plants and animals, including coal, oil, and natural gas."},
    {"text_input": "What is Framing?", "output": "Framing refers to the process of constructing a skeletal structure for buildings, typically using wood or metal."},
    {"text_input": "What is Fresh water aquatic ecotoxicity?", "output": "Freshwater aquatic ecotoxicity assesses the potential harmful effects of substances on freshwater ecosystems."},
    {"text_input": "What is G-value?", "output": "G-value is a measure of the solar heat gain through a glazing material, indicating its effectiveness in controlling heat."},
    {"text_input": "What is Gasification?", "output": "Gasification is a process that converts organic or fossil-based carbonaceous materials into carbon monoxide, hydrogen, and carbon dioxide."},
    {"text_input": "What is a Gateway?", "output": "A Gateway connects different networks and allows communication between devices within those networks."},
    {"text_input": "What is Geofencing?", "output": "Geofencing is a technology that creates virtual geographic boundaries, triggering responses when devices enter or exit those areas."},
    {"text_input": "What is Geolocation?", "output": "Geolocation is the identification of the geographic location of a person or device using digital information."},
    {"text_input": "What is Geotextile?", "output": "Geotextile is a synthetic textile used in civil engineering to reinforce soil and prevent erosion."},
    {"text_input": "What is Geothermal energy?", "output": "Geothermal energy is heat energy derived from the Earths internal heat sources."},
    {"text_input": "What is Global Warming Potential (GWP)?", "output": "Global Warming Potential (GWP) is a measure of how much a given mass of greenhouse gas contributes to global warming."},
    {"text_input": "What is Google Assistant?", "output": "Google Assistant is a virtual assistant powered by artificial intelligence, capable of performing tasks and providing information."},
    {"text_input": "What is Google Home?", "output": "Google Home is a smart speaker and home assistant device that uses Google Assistant for voice-activated tasks."},
    {"text_input": "What are Green Building Standards?", "output": "Green Building Standards are guidelines that promote sustainable building practices and energy efficiency."},
    {"text_input": "What is Green Electricity?", "output": "Green Electricity is power generated from renewable energy sources, such as wind or solar."},
    {"text_input": "What is the Green Guide to Specification?", "output": "The Green Guide to Specification is a resource that provides information on sustainable materials and construction practices."},
    {"text_input": "What is Green Power?", "output": "Green Power is energy generated from renewable resources that have a lower impact on the environment."},
    {"text_input": "What is the Green Register?", "output": "The Green Register is a certification scheme promoting sustainability and environmental awareness in the construction industry."},
    {"text_input": "What is a Green roof?", "output": "A Green roof is a roof that is partially or completely covered with vegetation, providing insulation and reducing runoff."},
    {"text_input": "What are Greenhouse gases?", "output": "Greenhouse gases are gases in the Earth's atmosphere that trap heat, contributing to climate change."},
    {"text_input": "What is Greenwash?", "output": "Greenwash refers to deceptive marketing practices that falsely claim a product or service is environmentally friendly."},
    {"text_input": "What is Greywater?", "output": "Greywater is wastewater generated from household activities like washing dishes and showering, often reused for irrigation."},
    {"text_input": "What is Greywater Reuse?", "output": "Greywater Reuse involves recycling greywater for non-potable applications, such as irrigation."},
    {"text_input": "What is a Ground source heat pump (GSHP)?", "output": "A Ground source heat pump (GSHP) is a system that uses the Earths thermal energy for heating and cooling buildings."},
    {"text_input": "What is Groundwater?", "output": "Groundwater is water that fills the cracks and spaces in underground soil and rock layers."},
    {"text_input": "What is Hazardous waste?", "output": "Hazardous waste is waste material that poses a significant risk to human health or the environment."},
    {"text_input": "What is Heat capacity?", "output": "Heat capacity is the amount of heat energy required to raise the temperature of a substance."},
    {"text_input": "What is a Heat exchanger?", "output": "A Heat exchanger is a system that transfers heat between two or more fluids without mixing them."},
    {"text_input": "What is a Heat island?", "output": "A Heat island is an urban area that experiences higher temperatures than its surrounding rural areas due to human activities."},
    {"text_input": "What is Heat Loss Parameter (HLP)?", "output": "Heat Loss Parameter (HLP) measures the rate of heat loss in a building relative to its volume."},
    {"text_input": "What is a Heat Pump?", "output": "A Heat Pump is a device that transfers heat energy from a source to a destination, often used for heating and cooling."},
    {"text_input": "What is Heat recovery?", "output": "Heat recovery refers to capturing waste heat from processes to use it for heating purposes."},
    {"text_input": "What is a Heat Recovery Ventilator?", "output": "A Heat Recovery Ventilator (HRV) is a system that exchanges indoor and outdoor air while recovering heat."},
    {"text_input": "What are Hot spots?", "output": "Hot spots are areas in a building that experience significantly higher temperatures than surrounding areas."},
    {"text_input": "What is Home Automation?", "output": "Home Automation is the use of technology to control household systems and devices remotely."},
    {"text_input": "What is a Home Energy Rating System?", "output": "A Home Energy Rating System evaluates a home's energy efficiency and provides a rating."},
    {"text_input": "What is a Home ID?", "output": "A Home ID is a unique identifier for a smart home system or device."},
    {"text_input": "What is HomeKit?", "output": "HomeKit is a framework by Apple that allows users to configure and control smart home devices."},
    {"text_input": "What is a Hub?", "output": "A Hub is a central device that connects and manages multiple smart devices within a home network."},
    {"text_input": "What is Hubitat?", "output": "Hubitat is a home automation platform that allows users to control smart devices locally."},
    {"text_input": "What is Human toxicity?", "output": "Human toxicity refers to the potential harmful effects of substances on human health."},
    {"text_input": "What is Humidity?", "output": "Humidity is the amount of water vapor present in the air."},
    {"text_input": "What are Hydrocarbons?", "output": "Hydrocarbons are organic compounds consisting solely of hydrogen and carbon, commonly found in fossil fuels."},
    {"text_input": "What is Hydrochlorofluorocarbon (HCFC)?", "output": "Hydrochlorofluorocarbon (HCFC) is a group of chemicals used in refrigeration and air conditioning, contributing to ozone depletion."},
    {"text_input": "What is Hydrofluorocarbon (HFC)?", "output": "Hydrofluorocarbon (HFC) is a greenhouse gas used in refrigeration and air conditioning systems."},
    {"text_input": "What is a Hygroscopic material?", "output": "A Hygroscopic material is one that absorbs moisture from the air."},
    {"text_input": "What is an Ice Dam?", "output": "An Ice Dam is a ridge of ice that forms at the edge of a roof, preventing melting snow from draining off."},
    {"text_input": "What is an Impermeable surface?", "output": "An Impermeable surface is one that does not allow water to pass through, leading to increased runoff."},
    {"text_input": "What is Indoor air quality (IAQ)?", "output": "Indoor air quality (IAQ) refers to the condition of air within buildings, affecting occupants' health and comfort."},
    {"text_input": "What is an Insulated Concrete Form?", "output": "An Insulated Concrete Form (ICF) is a system of insulated concrete wall forms that stay in place as part of the building structure."},
    {"text_input": "What is Insulated Glass?", "output": "Insulated Glass is a type of window construction that uses multiple layers of glass with insulating gas in between."},
    {"text_input": "What is Insulating concrete formwork (ICF)?", "output": "Insulating concrete formwork (ICF) consists of modular units that create a form for pouring concrete, providing insulation."},
    {"text_input": "What is an Intelligent building?", "output": "An Intelligent building is one that uses advanced technology to enhance efficiency, comfort, and sustainability."},
    {"text_input": "What is Insulation?", "output": "Insulation is a material used to reduce heat transfer between different areas, enhancing energy efficiency."},
    {"text_input": "What is Integration?", "output": "Integration refers to the combination of different systems or components to function as a cohesive unit."},
    {"text_input": "What are Internal heat gains?", "output": "Internal heat gains are the heat generated within a building from occupants, appliances, and equipment."},
    {"text_input": "What is the Internet of Things (IoT)?", "output": "The Internet of Things (IoT) refers to the network of physical devices connected to the internet, enabling data exchange."},
    {"text_input": "What is Interstitial condensation?", "output": "Interstitial condensation occurs when warm, moist air penetrates building materials and cools, causing moisture to form inside."},
    {"text_input": "What is a K-value?", "output": "A K-value is a measure of thermal conductivity, indicating how well a material conducts heat."},
    {"text_input": "What is a Kiosk?", "output": "A Kiosk is a small, standalone structure used for information or services, often found in public areas."},
    {"text_input": "What is Land use?", "output": "Land use refers to the management and modification of natural environments for various human activities."},
    {"text_input": "What is a Life cycle assessment (LCA)?", "output": "A Life cycle assessment (LCA) is a technique for assessing the environmental impacts of a product throughout its life cycle."},
    {"text_input": "What is a Life cycle costing (LCC)?", "output": "Life cycle costing (LCC) evaluates the total cost of ownership of a product or building over its entire lifespan."},
    {"text_input": "What is a Life cycle approach?", "output": "A Life cycle approach considers the environmental impacts of a product from raw material extraction to disposal."},
    {"text_input": "What is Light pollution?", "output": "Light pollution refers to excessive or misdirected artificial light that disrupts natural darkness."},
    {"text_input": "What is a Living Building?", "output": "A Living Building is a building that produces more energy than it consumes and has a positive environmental impact."},
    {"text_input": "What is Low-Emissivity (Low-E) glass?", "output": "Low-Emissivity (Low-E) glass is coated to reduce heat transfer and improve energy efficiency in windows."},
    {"text_input": "What is Low-impact development (LID)?", "output": "Low-impact development (LID) is a land planning approach that aims to manage stormwater and minimize environmental impact."},
    {"text_input": "What is Low-Voltage lighting?", "output": "Low-Voltage lighting uses less than 50 volts, providing energy-efficient lighting solutions."},
    {"text_input": "What is a MERV rating?", "output": "A MERV rating indicates the effectiveness of air filters at capturing airborne particles."},
    {"text_input": "What is a Microgrid?", "output": "A Microgrid is a localized energy system that can operate independently or in conjunction with the main grid."},
    {"text_input": "What is Microplastics?", "output": "Microplastics are small plastic particles less than 5mm in size, often resulting from the breakdown of larger plastic items."},
    {"text_input": "What is Modular construction?", "output": "Modular construction involves creating buildings from pre-fabricated sections or modules."},
    {"text_input": "What is a Modular Home?", "output": "A Modular Home is a type of house built in sections in a factory and then assembled on-site."},
    {"text_input": "What is a Net-Zero Energy Building?", "output": "A Net-Zero Energy Building generates as much energy as it consumes over the course of a year."},
    {"text_input": "What is Non-Renewable energy?", "output": "Non-Renewable energy comes from sources that cannot be replenished within a human timescale, such as fossil fuels."},
    {"text_input": "What is Offsetting?", "output": "Offsetting is the practice of balancing carbon emissions by investing in projects that reduce greenhouse gases."},
    {"text_input": "What is Onsite renewable energy?", "output": "Onsite renewable energy is energy generated from renewable sources located directly at a building site."},
    {"text_input": "What is Open-loop geothermal?", "output": "Open-loop geothermal systems use groundwater directly as a heat source or sink."},
    {"text_input": "What is a Passive house?", "output": "A Passive house is an energy-efficient building design that maintains comfort with minimal energy use."},
    {"text_input": "What is Passive Solar Design?", "output": "Passive Solar Design optimizes a building's orientation and materials to naturally regulate temperature using sunlight."},
    {"text_input": "What is Photovoltaic (PV) energy?", "output": "Photovoltaic (PV) energy is generated by converting sunlight directly into electricity using solar cells."},
    {"text_input": "What is Pollinator-friendly design?", "output": "Pollinator-friendly design incorporates features that support and attract pollinators, such as bees and butterflies."},
    {"text_input": "What is a Pollutant?", "output": "A Pollutant is a substance that causes harm to the environment or human health."},
    {"text_input": "What is a Pre-Assessment?", "output": "A Pre-Assessment evaluates a building's potential for sustainability before design or construction begins."},
    {"text_input": "What is a Prescriptive approach?", "output": "A Prescriptive approach in building design involves following specific guidelines or standards for construction."},
    {"text_input": "What is a Proximity sensor?", "output": "A Proximity sensor detects the presence of objects without physical contact."},
    {"text_input": "What is a Rain garden?", "output": "A Rain garden is a planted depression designed to absorb rainwater runoff from impervious surfaces."},
    {"text_input": "What is Renewable energy?", "output": "Renewable energy comes from sources that can be replenished naturally, such as solar, wind, and hydro."},
    {"text_input": "What is a Retrofitting?", "output": "Retrofitting involves adding new technology or features to existing buildings to improve performance."},
    {"text_input": "What is a Roof garden?", "output": "A Roof garden is a green space created on a building's roof, providing insulation and habitat for wildlife."},
    {"text_input": "What is a Roof overhang?", "output": "A Roof overhang is an extension of the roof beyond the walls of a building, providing shade and protection."},
    {"text_input": "What is Runoff?", "output": "Runoff is the flow of water over land, often leading to erosion and water pollution."},
    {"text_input": "What is a Sanitary landfill?", "output": "A Sanitary landfill is a site for the disposal of waste, designed to minimize environmental impact."},
    {"text_input": "What is Scaffolding?", "output": "Scaffolding is a temporary structure used to support workers and materials during construction."},
    {"text_input": "What is Smart Building Technology?", "output": "Smart Building Technology uses automated systems to enhance building efficiency, comfort, and safety."},
    {"text_input": "What is Smart Grid?", "output": "Smart Grid is an electrical grid that uses digital technology to monitor and manage the transport of electricity."},
    {"text_input": "What is Smart Meter?", "output": "A Smart Meter is an electronic device that records energy consumption in real-time."},
    {"text_input": "What is Solar thermal energy?", "output": "Solar thermal energy uses sunlight to generate heat, often for water heating or space heating."},
    {"text_input": "What is Solar shading?", "output": "Solar shading refers to techniques used to reduce heat gain in buildings from sunlight."},
    {"text_input": "What is a Solar tracker?", "output": "A Solar tracker is a device that orients solar panels toward the sun for maximum energy capture."},
    {"text_input": "What is a Solar wall?", "output": "A Solar wall is a wall designed to absorb solar energy and transfer heat to a building."},
    {"text_input": "What is Sustainable Architecture?", "output": "Sustainable Architecture focuses on designing buildings that are environmentally responsible and resource-efficient."},
    {"text_input": "What is Sustainable Development?", "output": "Sustainable Development meets the needs of the present without compromising the ability of future generations to meet theirs."},
    {"text_input": "What is Sustainable Materials?", "output": "Sustainable Materials are resources that have minimal environmental impact and can be replenished naturally."},
    {"text_input": "What is a Smart Building?", "output": "A Smart Building uses technology to monitor and control systems for improved efficiency and comfort."},
    {"text_input": "What is a Smart Home?", "output": "A Smart Home integrates technology to automate and enhance household functions and security."},
    {"text_input": "What is a Smart HVAC system?", "output": "A Smart HVAC system uses technology to optimize heating, ventilation, and air conditioning for energy efficiency."},
    {"text_input": "What is a Smart thermostat?", "output": "A Smart thermostat is a device that learns a user's preferences and adjusts heating and cooling accordingly."},
    {"text_input": "What is a Solar panel?", "output": "A Solar panel is a device that converts sunlight into electricity using photovoltaic cells."},
    {"text_input": "What is a Solar water heater?", "output": "A Solar water heater is a system that uses sunlight to heat water for domestic use."},
    {"text_input": "What is Stormwater management?", "output": "Stormwater management is the practice of controlling runoff from rainfall to minimize flooding and pollution."},
    {"text_input": "What is Sustainable Urban Development?", "output": "Sustainable Urban Development promotes urban growth that meets economic, social, and environmental goals."},
    {"text_input": "What is a Sustainability report?", "output": "A Sustainability report is a document outlining an organization's environmental performance and impact."},
    {"text_input": "What is Sustainable design?", "output": "Sustainable design is an approach to creating buildings that minimize environmental impact and resource use."},
    {"text_input": "What is a Thermal bridge?", "output": "A Thermal bridge is a section of a building that has a significantly higher heat transfer rate than the surrounding materials."},
    {"text_input": "What is a Thermal envelope?", "output": "A Thermal envelope is the barrier separating the interior of a building from the exterior environment, affecting energy efficiency."},
    {"text_input": "What is a Thermal mass?", "output": "Thermal mass is a material's ability to absorb and store heat energy, helping to regulate indoor temperatures."},
    {"text_input": "What is a Thermal transmittance?", "output": "Thermal transmittance measures the rate at which heat flows through a building element, influencing energy efficiency."},
    {"text_input": "What is a Urban heat island?", "output": "An Urban heat island is an urban area that is significantly warmer than its surrounding rural areas due to human activities."},
    {"text_input": "What is a Urban Planning?", "output": "Urban Planning is the process of designing and regulating land use and development in urban areas."},
    {"text_input": "What is a Ventilation?", "output": "Ventilation is the process of exchanging indoor air with outdoor air to maintain air quality."},
    {"text_input": "What is a Vertical garden?", "output": "A Vertical garden is a gardening technique where plants are grown vertically on structures, maximizing space."},
    {"text_input": "What is a Water-efficient landscaping?", "output": "Water-efficient landscaping uses plants and techniques that minimize water use while maintaining aesthetic appeal."},
    {"text_input": "What is Water Harvesting?", "output": "Water Harvesting is the collection and storage of rainwater for later use."},
    {"text_input": "What is a Water Recycling?", "output": "Water Recycling is the process of treating and reusing wastewater for various applications."},
    {"text_input": "What is a Waterway?", "output": "A Waterway is a navigable body of water that can be used for transportation."},
    {"text_input": "What is a Wetland?", "output": "A Wetland is a land area that is saturated with water, either permanently or seasonally, providing habitat and ecological functions."},
    {"text_input": "What is a Wind turbine?", "output": "A Wind turbine is a device that converts wind energy into electricity."},
    {"text_input": "What is a Zero-energy building?", "output": "A Zero-energy building is a structure that produces as much energy as it consumes, often through renewable sources."},
    {"text_input": "What is a Zoning?", "output": "Zoning is the process of dividing land into sections for different uses, such as residential, commercial, or industrial."}
]

    base_model = "models/gemini-1.5-flash-001-tuning"
    try:
        # Create a tuned model
        operation = genai.create_tuned_model(
            display_name="Real Estate Glossary Model",
            source_model=base_model,
            epoch_count=20,
            batch_size=4,
            learning_rate=0.001,
            training_data=training_data,
        )
        print("Fine-tuning started...")

        # Wait for the operation to complete
        for status in operation.wait_bar():
            print(f"Current status: {status}")
            time.sleep(10)

        result = operation.result()
        print("Tuned Model Created: ", result)

        return jsonify({"message": "Tuned model created successfully!", "model_name": result.name}), 200
    except Exception as e:
        print("Error during fine-tuning:", str(e))
        return jsonify({"error": "Failed to create a tuned model."}), 500
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
