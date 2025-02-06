import streamlit as st
import subprocess
import platform
import speedtest
import plotly.graph_objects as go
import re

# Function to navigate between pages
def switch_page(page):
    st.session_state["page"] = page
    st.rerun()  # Replace st.experimental_rerun() with st.rerun()

# Function to execute ping
def ping_website(website):
    try:
        result = subprocess.run(
            ["ping", "-n", "4", website] if platform.system() == "Windows" else ["ping", "-c", "4", website],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return str(e)

# Function to execute nslookup
def nslookup_website(website):
    try:
        result = subprocess.run(["nslookup", website], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return str(e)

# Function to execute traceroute
def check_connection_path(website):
    try:
        command = ["tracert", website] if platform.system() == "Windows" else ["traceroute", website]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return str(e)

# Function to get network details
def get_network_details():
    try:
        command = ["ipconfig"] if platform.system() == "Windows" else ["ifconfig"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        output = result.stdout
        # Extract IPv4 & IPv6
        ipv4_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        ipv6_pattern = r"\b(?:[A-Fa-f0-9:]+:+)+[A-Fa-f0-9]+\b"
        ipv4_addresses = re.findall(ipv4_pattern, output)
        ipv6_addresses = re.findall(ipv6_pattern, output)
        formatted_output = "### IP Addresses ###\n"
        if ipv4_addresses:
            formatted_output += f"IPv4: {ipv4_addresses[0]}\n"
        if ipv6_addresses:
            formatted_output += f"IPv6: {ipv6_addresses[0]}\n"
        formatted_output += "\n### Full Network Details ###\n" + output
        return formatted_output
    except Exception as e:
        return str(e)

# Function to execute netstat
def check_active_connections():
    try:
        command = ["netstat", "-a"] if platform.system() == "Windows" else ["netstat", "-an"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return str(e)

# Function to run speed test
def run_speed_test():
    st.write("⚡ Running Speed Test... Please wait.")
    stt = speedtest.Speedtest()
    stt.get_best_server()
    # Get download and upload speeds in Mbps
    download_speed = stt.download() / 1_000_000  # Convert from bps to Mbps
    upload_speed = stt.upload() / 1_000_000  # Convert from bps to Mbps
    ping = stt.results.ping
    return download_speed, upload_speed, ping

# Function to create speedometer (Gauge Chart)
def create_speedometer(speed, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=speed,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 100]},  # Set max speed to 100 Mbps
            'bar': {'color': "blue"},
            'steps': [
                {'range': [0, 20], 'color': "red"},
                {'range': [20, 50], 'color': "orange"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "green"}
            ],
        }))
    return fig

# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Navigation system
if st.session_state["page"] == "home":
    st.title("🌐 Network Tools")
    st.markdown("Choose a tool below:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Ping a Website"):
            switch_page("ping")
        if st.button("🌍 Find Website Details (NSLookup)"):
            switch_page("nslookup")
        if st.button("🛤 Trace Route to Website"):
            switch_page("traceroute")
    with col2:
        if st.button("🖥 Show My Network Details (IPConfig)"):
            switch_page("ipconfig")
        if st.button("📡 Check Active Connections (Netstat)"):
            switch_page("netstat")
        if st.button("⚡ Run Speed Test"):
            switch_page("speedtest")
elif st.session_state["page"] == "ping":
    st.title("🔍 Ping a Website")
    website = st.text_input("Enter a website:")
    if website and st.button("Run Ping"):
        st.text_area("Ping Results", ping_website(website), height=300)
    if st.button("⬅ Back"):
        switch_page("home")
elif st.session_state["page"] == "nslookup":
    st.title("🌍 Find Website Details (NSLookup)")
    website = st.text_input("Enter a website:")
    if website and st.button("Run NSLookup"):
        st.text_area("NSLookup Results", nslookup_website(website), height=300)
    if st.button("⬅ Back"):
        switch_page("home")
elif st.session_state["page"] == "traceroute":
    st.title("🛤 Trace Route to Website")
    website = st.text_input("Enter a website:")
    if website and st.button("Run Traceroute"):
        st.text_area("Traceroute Results", check_connection_path(website), height=300)
    if st.button("⬅ Back"):
        switch_page("home")
elif st.session_state["page"] == "ipconfig":
    st.title("🖥 My Network Details (IPConfig)")
    if st.button("Run Test"):
        st.text_area("Network Details", get_network_details(), height=300)
    if st.button("⬅ Back"):
        switch_page("home")
elif st.session_state["page"] == "netstat":
    st.title("📡 Active Internet Connections (Netstat)")
    if st.button("Run Test"):
        st.text_area("Active Connections", check_active_connections(), height=300)
    if st.button("⬅ Back"):
        switch_page("home")
elif st.session_state["page"] == "speedtest":
    st.title("⚡ Internet Speed Test")
    if st.button("Run Speed Test"):
        download_speed, upload_speed, ping = run_speed_test()
        st.metric("📥 Download Speed", f"{download_speed:.2f} Mbps")
        st.metric("📤 Upload Speed", f"{upload_speed:.2f} Mbps")
        st.metric("📶 Ping", f"{ping} ms")
        st.plotly_chart(create_speedometer(download_speed, "Download Speed"), use_container_width=True)
        st.plotly_chart(create_speedometer(upload_speed, "Upload Speed"), use_container_width=True)
    if st.button("⬅ Back"):
        switch_page("home")
