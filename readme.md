\# Koplenti ACStorage for Home Assistant



Custom Home Assistant integration to control and monitor the `AcStorage` setting of Kostal inverters via `pykoplenti`.



This integration exposes the `devices:local/EnergyMgmt:AcStorage` value as a Home Assistant switch and adds diagnostic logging and status monitoring.



\---



\## Features



\- ACStorage switch control

\- Periodic polling of inverter state

\- Detects external changes (e.g. inverter web UI)

\- Detailed logging sensor

\- Multi-inverter support

\- Home Assistant 2025 compatible

\- Config Flow support

\- Local polling

\- HACS-ready



\---



\## Requirements



\- Home Assistant 2025+

\- Python package `pykoplenti`

\- Access to your Kostal inverter(s)

\- Master password and service code



\---



\## Installation



\### HACS (Custom Repository)



1\. Open HACS

2\. Integrations

3\. Three dots → Custom repositories

4\. Add:



https://github.com/slauf82/koplenti\_acstorage



Category:



Integration



5\. Install

6\. Restart Home Assistant



\---



\## Manual Installation



Copy:



custom\_components/koplenti\_acstorage



to:



/config/custom\_components/



Restart Home Assistant afterwards.



\---



\## Configuration



Go to:



Settings → Devices \& Services → Add Integration



Search for:



Koplenti ACStorage



You will need:



\- Inverter IP address

\- Master password

\- Service code



\---



\## Entities



\### Switch



Example:



switch.koplenti\_acstorage\_170



Controls the ACStorage state of the inverter.



\---



\### Log Sensor



Example:



sensor.koplenti\_log\_170



Provides:



\- log count as sensor state

\- detailed log messages in attributes



Useful for debugging and automation diagnostics.



\---



\## How it works



The integration uses:



pykoplenti read-settings  

pykoplenti write-settings



to read and modify:



devices:local/EnergyMgmt:AcStorage



The switch state is periodically verified and synchronized with the inverter.



\---



\## Polling



Default polling interval:



10 seconds



This ensures Home Assistant also detects changes made directly in the inverter web interface.



\---



\## Logging



The integration includes extensive debug logging:



\- switch actions

\- read/write attempts

\- retries

\- inverter responses

\- synchronization events



Logs are available:



\- in Home Assistant system logs

\- via the log sensor entity



\---



\## Multi-Inverter Support



The integration supports multiple inverter instances simultaneously.



Entity names automatically include the last octet of the inverter IP address:



switch.koplenti\_acstorage\_170  

switch.koplenti\_acstorage\_172



\---



\## Example Use Cases



\- PV surplus charging

\- Zero-export control

\- Sequential battery charging

\- Home Assistant energy management

\- Preventing unnecessary grid export



\---



\## Known Limitations



\- ACStorage changes may take several seconds to become active

\- Inverter response times can vary

\- Polling-based synchronization is intentionally conservative for stability



\---



\## Troubleshooting



\### Switch resets automatically



Increase delays and retry intervals.



The integration is optimized for stability rather than aggressive switching.



\---



\### State differs from inverter UI



Wait for the next polling cycle.



Default:



10 seconds



\---



\### No entities appear



Check Home Assistant logs:



Settings → System → Logs



\---



\## Roadmap



Planned ideas:



\- Additional inverter diagnostics

\- Enhanced energy management features

\- Dynamic charge prioritization

\- Advanced balancing strategies

\- Improved HACS metadata



\---



\## Credits



Built for Home Assistant and Kostal inverter users using `pykoplenti`.



\---



\## License



GNU General Public License v3.0



This project is licensed under the GNU GPL v3.0 License.

