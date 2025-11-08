# Week 11 – Advanced Configuration & Access Control

## Objective

This week, you’ll implement **basic authentication** and **configuration management**
to make your monitoring dashboard behave like a real system administration tool.

---

## Tasks

1. Implement a simple login form using Streamlit
   - Username: `admin`
   - Password: `admin123`
2. Store login state using `st.session_state`
3. Add a **Configuration Panel** with sliders to adjust thresholds:
   - CPU Threshold
   - Memory Threshold
   - Disk Threshold
4. Add a **Logout** option that resets the session
5. Keep the Dashboard page displaying data from `log.db`

---

## Example Output

- Login page with username/password form  
- Dashboard showing last 10 entries and charts  
- Configuration panel with adjustable sliders  
- Logout resets the interface  

---

## Run the Dashboard

```bash
streamlit run app.py
```

## Submission Checklist

 Login and Logout functions implemented

 Threshold sliders visible under Configuration

 Dashboard connected to log.db

 Screenshot showing all three pages (Login, Dashboard, Configuration)
---

## Bonus (Optional)

Store user credentials in a database instead of hardcoding

Apply new thresholds to filter alert data dynamically

Add role-based access (admin vs user)
