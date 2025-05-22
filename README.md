# 🌐 Network Tools Dashboard
A simple and interactive Streamlit-based network utility tool for diagnosing and testing your internet connection. This tool offers a visual, easy-to-use interface for common network commands like ping, nslookup, traceroute, and more — no terminal required!

A simple and interactive Streamlit-based network utility tool for diagnosing and testing your internet connection. This tool offers a visual, easy-to-use interface for common network commands like ping, nslookup, traceroute, and more — no terminal required!

🚀 Features
🔍 Ping a website to check its reachability.

🌍 Perform an NSLookup to fetch DNS information.

🛤 Trace the network route to a domain.

🖥 View your local network configuration (IP addresses, etc.).

📡 Check active internet connections via netstat.

⚡ Run an internet speed test and view results with gauge visualizations (using Plotly).

🛠 Installation
Requirements
Python 3.7+

streamlit

plotly

speedtest-cli

Install dependencies

pip install streamlit plotly speedtest-cli

📦 How to Run

streamlit run network_tool.py

🧠 How It Works

Each page is a tool:

Ping: Uses ping via subprocess.

NSLookup: Uses nslookup via subprocess.

Traceroute: Uses traceroute or tracert based on the OS.

IPConfig: Displays IP details by parsing ipconfig/ifconfig output.

Netstat: Shows all current connections via netstat.

Speed Test: Uses speedtest-cli to show upload/download/ping.

🖼 UI/UX Highlights

Built-in page navigation using st.session_state.

Interactive forms and buttons per feature.

Speed test results visualized as speedometers via Plotly Gauge Charts.

📌 Notes
The app uses OS commands and may behave differently on Windows, macOS, and Linux.

Some features require network or admin permissions (e.g., netstat).

🙌 Acknowledgements

Streamlit

Plotly

speedtest-cli
