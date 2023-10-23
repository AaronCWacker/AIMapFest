import streamlit as st

# Game list and associated icons
games = [
    'Terraforming Mars', 
    'Twilight Imperium (Fourth Edition)', 
    'Scythe', 
    'Eclipse', 
    'Small World', 
    'Risk Legacy', 
    'Axis & Allies', 
    'Diplomacy', 
    'Pandemic Legacy: Season 1', 
    'Brass: Birmingham'
]

icons = ['🪐', '🚀', '🤖', '🌌', '🧝‍♂️', '🗺️', '⚔️', '🤝', '🦠', '🏭']

# Main code
st.title('Top Ten Board Games with Map-Making Strategies 🗺️')

for i, (game, icon) in enumerate(zip(games, icons)):
    st.markdown(f"{i + 1}. {game} {icon}")

    # Expanders for each game to outline map rules or strategies
    with st.expander(f"See Map Building & Gamification Strategy for {game}"):
        
        if game == 'Terraforming Mars':
            st.markdown("""
            🪐 **Terraforming Mars Map Strategies**
            1. 🌱 Opt for plant-heavy areas
            2. 💧 Prioritize water tiles
            3. 🏭 Position factories near energy resources
            4. 🌋 Leverage volcanic areas
            5. 🌐 Control key global parameters
            6. 💡 Plan your energy grid
            7. 🛤️ Connect your colonies
            8. 🌡️ Master temperature control
            9. 🎯 Aim for synergies
            10. 🚀 Upgrade spaceports for max mobility
            """)

        elif game == 'Twilight Imperium (Fourth Edition)':
            st.markdown("""
            🚀 **Twilight Imperium Map Strategies**
            1. 🌌 Position fleets in strategic nebulas
            2. 🏰 Fortify chokepoints
            3. ⚖️ Balance resources among systems
            4. 🌐 Establish effective trade routes
            5. 🛡️ Use PDS systems wisely
            6. 🌀 Be cautious around wormholes
            7. 🌟 Prioritize Mecatol Rex
            8. 🌕 Use moons for surprise attacks
            9. 🛠️ Optimize unit upgrades
            10. 🤝 Forge strategic alliances
            """)

        elif game == 'Scythe':
            st.markdown("""
            🤖 **Scythe Map Strategies**
            1. 🏞️ Choose starting positions wisely
            2. 🛠️ Optimize for factory cards
            3. 🗺️ Be aware of your neighbors
            4. 🌊 Control rivers for mobility
            5. 🏭 Maximize resource buildings
            6. 🛡️ Guard against backdoor attacks
            7. 🎯 Focus on objectives
            8. 🌾 Manage food resources
            9. 🎲 Play the probabilities
            10. 💎 Hunt for treasures
            """)
