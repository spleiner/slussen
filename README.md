# SLussen 🚌

*En Streamlit-app för att visa realtidsavgångar för bussar från Slussen till Nacka/Värmdö*

[English](#english) | [Svenska](#svenska)

## Svenska

### Översikt

SLussen är en webbapplikation som visar realtidsavgångar för bussar från Slussen i Stockholm mot Nacka och Värmdö. Appen hämtar data från Stockholms Lokaltrafiks (SL) öppna API:er och uppdateras automatiskt varje minut.

### Funktioner

- **Realtidsavgångar**: Visar kommande bussar med förväntade avgångstider
- **Flera hållplatser**: Täcker avgångar från Slussen, Slussbrogatan och Glasbruksgatan
- **Linjefiltrering**: Möjlighet att välja specifika busslinjer
- **Trafikstörningar**: Visar aktuella trafikavbrott och störningar
- **Automatisk uppdatering**: Data uppdateras varje minut
- **Responsiv design**: Fungerar på desktop och mobil

### Busslinjer som täcks

Appen visar avgångar för följande busslinjer mot Nacka/Värmdö:
- **Huvudlinjer**: 401, 402, 409, 410, 413, 414, 420, 422, 425
- **Express-/Pendlingsbussar**: 428X, 429X, 430X
- **Lokala linjer**: 432-445, 471, 474, 491, 496, 497
- **Marknadslinjer**: 25M, 26M
- **Övriga**: 423, 449, 71T

### Installation och körning

#### Förutsättningar
- Python 3.8+
- pip (Python package manager)

#### Lokal installation

1. **Klona repositoriet**:
   ```bash
   git clone https://github.com/spleiner/slussen.git
   cd slussen
   ```

2. **Installera beroenden**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Kör applikationen**:
   ```bash
   streamlit run slussen.py
   ```

4. **Öppna webbläsaren** och gå till `http://localhost:8501`

#### Deployment på Streamlit Cloud

1. Forka detta repository till ditt GitHub-konto
2. Gå till [share.streamlit.io](https://share.streamlit.io)
3. Anslut ditt GitHub-konto och välj repositoriet
4. Applikationen kommer att deployas automatiskt

### Användning

1. **Öppna applikationen** i din webbläsare
2. **Välj busslinjer**: 
   - Markera "Alla bussar" för att se alla linjer
   - Avmarkera och välj specifika linjer från listan
3. **Visa avgångar**: Tabellen visar linje, destination, avgångstid och hållplats
4. **Kontrollera störningar**: Eventuella trafikstörningar visas överst
5. **Uppdatera**: Klicka "Uppdatera" eller vänta på automatisk uppdatering

### API-information

Applikationen använder följande SL-API:er:
- **Departures API**: Hämtar realtidsavgångar från hållplatser
- **Deviations API**: Hämtar information om trafikstörningar

Hållplats-ID:n som används:
- Slussen: 9192
- Slussen (alternativ): 1321

### Utveckling

#### Projektstruktur
```
slussen/
├── slussen.py          # Huvudapplikation
├── requirements.txt    # Python-beroenden
├── README.md          # Denna fil
├── LICENSE            # MIT-licens
└── .github/
    └── workflows/
        └── ruff.yml   # CI/CD för kodkvalitet
```

#### Viktiga funktioner

- `fetch_departure_data()`: Hämtar avgångsdata från SL API
- `fetch_deviation_data()`: Hämtar störningsinformation
- `parse_departure_data()`: Bearbetar och filtrerar avgångsdata
- `display_deviations()`: Visar trafikstörningar i användargränssnittet

Se källkoden för detaljerad dokumentation av alla funktioner.

### Felsökning

**Problem**: Inga avgångar visas
- **Lösning**: Kontrollera internetanslutning, SL API kan vara tillfälligt otillgängligt

**Problem**: Appen laddar långsamt
- **Lösning**: Detta är normalt vid första laddning, efterföljande laddningar är snabbare tack vare cachning

**Problem**: Felaktig avgångstid
- **Lösning**: Data kommer direkt från SL, rapportera problem till SL:s kundtjänst

### Dokumentation

📚 **[Komplett Dokumentationsindex](DOCS.md)** - Hitta rätt dokumentation för dina behov

**För användare**:
- 📖 [Användarguide](USER_GUIDE.md) - Detaljerad guide för att använda applikationen
- 🚀 [Deployment Guide](DEPLOYMENT.md) - Instruktioner för att deploya applikationen

**För utvecklare**:
- 🤝 [Bidragsguidelines](CONTRIBUTING.md) - Hur man bidrar till projektet
- 🏗️ [Arkitekturdokumentation](ARCHITECTURE.md) - Teknisk arkitektur och design
- 🔌 [API-dokumentation](API.md) - Detaljerad information om externa och interna API:er
- 📝 [Changelog](CHANGELOG.md) - Versionshistorik och ändringar

### Bidrag

Vi välkomnar bidrag! Se [CONTRIBUTING.md](CONTRIBUTING.md) för riktlinjer.

### Licens

Detta projekt är licensierat under MIT-licensen - se [LICENSE](LICENSE) för detaljer.

### Författare

Skapad av [Stefan Pleiner](https://github.com/spleiner)

---

## English

### Overview

SLussen is a web application that displays real-time bus departures from Slussen in Stockholm to Nacka and Värmdö. The app fetches data from Stockholm Public Transport's (SL) open APIs and updates automatically every minute.

### Features

- **Real-time departures**: Shows upcoming buses with expected departure times
- **Multiple stops**: Covers departures from Slussen, Slussbrogatan, and Glasbruksgatan
- **Line filtering**: Option to select specific bus lines
- **Traffic disruptions**: Shows current traffic interruptions and disturbances
- **Automatic updates**: Data refreshes every minute
- **Responsive design**: Works on desktop and mobile

### Bus Lines Covered

The app shows departures for the following bus lines to Nacka/Värmdö:
- **Main lines**: 401, 402, 409, 410, 413, 414, 420, 422, 425
- **Express/Commuter buses**: 428X, 429X, 430X
- **Local lines**: 432-445, 471, 474, 491, 496, 497
- **Market lines**: 25M, 26M
- **Others**: 423, 449, 71T

### Installation and Running

#### Prerequisites
- Python 3.8+
- pip (Python package manager)

#### Local Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/spleiner/slussen.git
   cd slussen
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run slussen.py
   ```

4. **Open your browser** and go to `http://localhost:8501`

#### Deployment on Streamlit Cloud

1. Fork this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account and select the repository
4. The application will be deployed automatically

### Usage

1. **Open the application** in your browser
2. **Select bus lines**: 
   - Check "Alla bussar" (All buses) to see all lines
   - Uncheck and select specific lines from the list
3. **View departures**: The table shows line, destination, departure time, and stop
4. **Check disruptions**: Any traffic disruptions are shown at the top
5. **Refresh**: Click "Uppdatera" (Update) or wait for automatic refresh

### API Information

The application uses the following SL APIs:
- **Departures API**: Fetches real-time departures from stops
- **Deviations API**: Fetches traffic disruption information

Stop IDs used:
- Slussen: 9192
- Slussen (alternative): 1321

### Development

#### Project Structure
```
slussen/
├── slussen.py          # Main application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── LICENSE            # MIT license
└── .github/
    └── workflows/
        └── ruff.yml   # CI/CD for code quality
```

#### Key Functions

- `fetch_departure_data()`: Fetches departure data from SL API
- `fetch_deviation_data()`: Fetches disruption information
- `parse_departure_data()`: Processes and filters departure data
- `display_deviations()`: Displays traffic disruptions in the UI

See source code for detailed documentation of all functions.

### Troubleshooting

**Issue**: No departures shown
- **Solution**: Check internet connection, SL API may be temporarily unavailable

**Issue**: App loads slowly
- **Solution**: This is normal on first load, subsequent loads are faster due to caching

**Issue**: Incorrect departure time
- **Solution**: Data comes directly from SL, report issues to SL customer service

### Documentation

📚 **[Complete Documentation Index](DOCS.md)** - Find the right documentation for your needs

**For Users**:
- 📖 [User Guide](USER_GUIDE.md) - Comprehensive guide for using the application
- 🚀 [Deployment Guide](DEPLOYMENT.md) - Instructions for deploying the application

**For Developers**:
- 🤝 [Contributing Guidelines](CONTRIBUTING.md) - How to contribute to the project
- 🏗️ [Architecture Documentation](ARCHITECTURE.md) - Technical architecture and design
- 🔌 [API Documentation](API.md) - Detailed information about external and internal APIs
- 📝 [Changelog](CHANGELOG.md) - Version history and changes

### Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

### Author

Created by [Stefan Pleiner](https://github.com/spleiner)
