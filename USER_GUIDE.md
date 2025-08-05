# User Guide - SLussen

A comprehensive guide to using the SLussen application for viewing bus departures from Slussen to Nacka/Värmdö.

## Table of Contents

- [Getting Started](#getting-started)
- [Understanding the Interface](#understanding-the-interface)
- [Using the Application](#using-the-application)
- [Features Explained](#features-explained)
- [Tips and Tricks](#tips-and-tricks)
- [Troubleshooting](#troubleshooting)
- [Frequently Asked Questions](#frequently-asked-questions)

## Getting Started

### Accessing the Application

**Live Application**: Visit the deployed application at your provided URL

**Local Access**: If running locally, go to `http://localhost:8501`

### First Use

When you first open SLussen, you'll see:
1. A loading screen while data is fetched from Stockholm Public Transport (SL)
2. Any current traffic disruptions (if present)
3. A table of upcoming bus departures
4. Controls for filtering which bus lines to display

## Understanding the Interface

### Header Section

- **App Title**: "SLussen 🚌" 
- **About Menu**: Click the menu (☰) in the top-right for app information and bug reporting

### Traffic Disruptions (When Present)

```
🚨 Trafikstörningar
⚠️ Störning på linje 401
   På grund av trafikstörning kan förseningar uppstå på linje 401...
```

Traffic disruptions appear as an expandable red section at the top when there are significant service disruptions.

### Bus Line Selection

```
☑️ Alla bussar (avmarkera för att välja enskilda linjer)

□ Välj bussar
  Inga bussar valda
```

Control which bus lines you want to see:
- **"Alla bussar"**: Shows all available lines (default)
- **Individual Selection**: Uncheck "Alla bussar" to choose specific lines

### Departures Table

| Linje | Destination | Avgår | Hållplats |
|-------|-------------|-------|-----------|
| 401   | Nacka station | 3 min | A |
| 409   | Värmdö centrum | 7 min | B |
| 25M   | Marknadsplatsen | 12 min | Glasbruksgatan |

**Columns Explained**:
- **Linje**: Bus line number
- **Destination**: Final destination of the bus
- **Avgår**: Departure time (in minutes or actual time)
- **Hållplats**: Stop location/platform

### Update Button

```
[Uppdatera]
```

Click to manually refresh the data (automatic refresh happens every minute).

## Using the Application

### Viewing All Bus Departures

1. **Open the application**
2. **Ensure "Alla bussar" is checked** (default state)
3. **View the departures table** showing all buses to Nacka/Värmdö

### Filtering by Specific Bus Lines

1. **Uncheck "Alla bussar"**
2. **Click on "Välj bussar"** dropdown
3. **Select the bus lines** you're interested in:
   - Type line numbers to search (e.g., "401")
   - Click on line numbers to select/deselect
   - Multiple lines can be selected
4. **View filtered results** in the table

### Checking for Disruptions

1. **Look for the red section** at the top of the page
2. **Click to expand** if the disruption section is collapsed
3. **Read disruption details** for affected lines
4. **Plan accordingly** based on the information provided

### Manual Refresh

1. **Click "Uppdatera"** at the bottom of the page
2. **Wait for data to reload** (usually 1-2 seconds)
3. **View updated departure times**

## Features Explained

### Real-time Data

- **Data Source**: Stockholm Public Transport (SL) live APIs
- **Update Frequency**: Automatic refresh every 60 seconds
- **Accuracy**: Shows real-time delays and cancellations

### Intelligent Stop Mapping

The application automatically shows the correct stop location based on the bus line:

**Glasbruksgatan Stop**:
- Line 25M (Market line to Marknadsplatsen)
- Line 26M (Market line to Gustavsberg)
- Line 423 (Local service)
- Line 449 (Local service)

**Slussbrogatan Stop**:
- Line 71T (Tourist line)

**Regular Slussen Stops** (A, B, C, etc.):
- All other lines (401, 402, 409, etc.)

### Priority-based Disruption Filtering

Not all service messages are shown - only high-priority disruptions that significantly affect service:

- **High Priority**: Major delays, route changes, service cancellations
- **Medium Priority**: Minor delays, crowding information
- **Low Priority**: Routine maintenance notices (filtered out)

### Departure Time Display

The application shows departure times in the most helpful format:

- **"Nu"**: Departing now
- **"2 min"**: Departing in 2 minutes
- **"14:35"**: Actual departure time (for longer waits)
- **"--"**: No real-time data available

## Tips and Tricks

### Efficient Usage

**For Daily Commuters**:
1. Filter to only your regular lines
2. Bookmark the filtered URL for quick access
3. Check disruptions first thing in the morning

**For Occasional Users**:
1. Keep "Alla bussar" selected to see all options
2. Check destination carefully (some lines have multiple variants)
3. Note the stop location to find the correct platform

### Mobile Usage

- **Responsive Design**: Works well on smartphones and tablets
- **Touch-friendly**: Large buttons and touch targets
- **Offline Tolerance**: Cached data available briefly if connection is lost

### Understanding Destinations

**Common Destinations**:
- **Nacka station**: Main transport hub in Nacka
- **Värmdö centrum**: Shopping center in Värmdö
- **Gustavsberg**: Historic town with porcelain factory
- **Marknadsplatsen**: Nacka market square

**Express vs Local**:
- **Express lines (X suffix)**: Fewer stops, faster journey
- **Local lines**: More stops, serves local communities
- **Market lines (M suffix)**: Limited schedule, specific destinations

### Time Planning

- **Add buffer time**: Allow 2-3 minutes to walk to the stop
- **Peak hours**: More frequent service but potentially more crowded
- **Off-peak**: Less frequent but more reliable timing
- **Weekends**: Different schedules, check departure times carefully

## Troubleshooting

### Common Issues and Solutions

**Issue**: "Inga avgångar hittades" (No departures found)
- **Possible Causes**: 
  - Late evening/night (limited service)
  - Major service disruption
  - Technical issue with SL APIs
- **Solutions**:
  - Check current time (service may be limited)
  - Check SL's official website for major disruptions
  - Try refreshing the page
  - Wait a few minutes and try again

**Issue**: App loads slowly
- **Causes**: 
  - First-time loading (cache building)
  - Slow internet connection
  - SL API delays
- **Solutions**:
  - Wait 30-60 seconds for initial load
  - Check internet connection
  - Subsequent loads will be faster

**Issue**: Departure times seem wrong
- **Possible Causes**:
  - Real-time delays not reflected
  - Bus already departed
  - Data sync delay
- **Solutions**:
  - Cross-reference with SL app or station displays
  - Refresh the application
  - Allow for minor variations in real-time data

**Issue**: Missing bus lines
- **Possible Causes**:
  - Line not in service to Nacka/Värmdö
  - Temporary route changes
  - New lines not yet added to the application
- **Solutions**:
  - Verify line serves Nacka/Värmdö destinations
  - Check if "Alla bussar" is selected
  - Report missing lines via GitHub issues

**Issue**: Traffic disruptions not showing
- **Explanation**: Only high-priority disruptions are shown
- **Alternative**: Check SL's official app for all service notices

### Performance Issues

**Slow Loading**:
- Wait for initial cache to build (first use)
- Ensure stable internet connection
- Try refreshing the browser

**Frequent Errors**:
- Check internet connectivity
- SL APIs may be experiencing issues
- Try again later

### Browser Compatibility

**Supported Browsers**:
- Chrome (recommended)
- Firefox
- Safari
- Edge

**Mobile Browsers**:
- Chrome Mobile
- Safari Mobile
- Samsung Internet

## Frequently Asked Questions

### General Usage

**Q: How often is the data updated?**
A: The application fetches new data every 60 seconds automatically. You can also manually refresh by clicking "Uppdatera".

**Q: Why don't I see all bus lines to Nacka/Värmdö?**
A: The application only shows lines that regularly serve Nacka/Värmdö destinations. Special services or infrequent lines may not be included.

**Q: Can I see buses going in the opposite direction?**
A: No, this application specifically shows buses FROM Slussen TO Nacka/Värmdö. For return journeys, use SL's official app.

**Q: What does "Glasbruksgatan" vs regular stops mean?**
A: Different bus lines depart from different locations around Slussen. The application automatically shows the correct stop for each line.

### Technical Questions

**Q: Does the app work offline?**
A: No, the app requires an internet connection to fetch real-time data from SL's APIs.

**Q: Why do some departure times show actual times while others show minutes?**
A: Times close to departure (usually within 30 minutes) are shown as "X min", while further departures show actual times like "14:35".

**Q: Is my location tracked?**
A: No, the application doesn't access or store any location data. It only shows departure information for the fixed Slussen stops.

### Data and Accuracy

**Q: How accurate are the departure times?**
A: Times come directly from SL's real-time systems and are generally accurate within 1-2 minutes, but delays can occur due to traffic or operational issues.

**Q: Why might departure times differ from station displays?**
A: There can be slight sync delays between different SL systems. When in doubt, refer to physical station displays or SL's official app.

**Q: What happens if there's a major service disruption?**
A: High-priority disruptions will be displayed prominently at the top of the app. For detailed information, check SL's official channels.

### Support

**Q: I found a bug or have a feature request. Where can I report it?**
A: Please visit the GitHub repository and create an issue: [github.com/spleiner/slussen/issues](https://github.com/spleiner/slussen/issues)

**Q: Can I contribute to the project?**
A: Yes! The project welcomes contributions. See the [Contributing Guidelines](CONTRIBUTING.md) for details.

**Q: Is the source code available?**
A: Yes, SLussen is open source under the MIT license. The code is available on GitHub.

---

*For technical support or additional questions, please create an issue on GitHub or contact the maintainer.*