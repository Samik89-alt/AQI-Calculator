# AQI Calculator

This project calculates the **Air Quality Index (AQI)** from pollutant concentration values such as **PM2.5, PM10, SO₂, NO₂, CO, O₃, and NH₃**.

AQI is a numerical scale used to communicate **how polluted the air currently is** and the **potential health effects** associated with it.

The implementation follows the methodology defined by the **Central Pollution Control Board (CPCB), India**.

---

# Running the Program

```bash
python aqi_calculator.py
```

---

# Overview

The AQI Calculator takes **pollutant concentration values as input** and computes the **Air Quality Index** using standard CPCB guidelines.

The pollutants considered in this project include:

* PM2.5
* PM10
* SO₂
* NO₂
* CO
* O₃
* NH₃

The system calculates an **AQI sub-index for each pollutant** and determines the **final AQI** based on the highest sub-index.

---

# Core Concept

AQI is calculated in **two main steps**.

---

## 1️⃣ Calculate Sub-Index for Each Pollutant

Each pollutant concentration is converted into an **AQI sub-index** using **linear interpolation**.

### Formula

```
AQI_p = ((I_hi - I_lo) / (BP_hi - BP_lo)) × (C_p - BP_lo) + I_lo
```

### Where

* **AQI_p** = AQI sub-index for pollutant *p*
* **C_p** = Measured pollutant concentration
* **BP_lo** = Lower breakpoint of concentration range
* **BP_hi** = Upper breakpoint of concentration range
* **I_lo** = AQI value corresponding to BP_lo
* **I_hi** = AQI value corresponding to BP_hi

Breakpoints define pollutant ranges corresponding to **AQI categories**.

---

## 2️⃣ Determine Final AQI

After calculating the **sub-index for each pollutant**, the final AQI is calculated as:

```
AQI = max(PM2.5_subindex, PM10_subindex, SO2_subindex, NO2_subindex, CO_subindex, O3_subindex, NH3_subindex)
```

The **maximum sub-index becomes the final AQI**.

The pollutant responsible for the highest sub-index is called the **dominant pollutant**.

---

# AQI Categories

| AQI Range | Air Quality  |
| --------- | ------------ |
| 0 – 50    | Good         |
| 51 – 100  | Satisfactory |
| 101 – 200 | Moderate     |
| 201 – 300 | Poor         |
| 301 – 400 | Very Poor    |
| 401 – 500 | Severe       |

---

# Program Workflow

1. Take pollutant concentration values as input.
2. Determine the breakpoint range for each pollutant.
3. Calculate the **sub-index** using the interpolation formula.
4. Compute the **maximum sub-index**.
5. Output the **final AQI and air quality category**.

---

# Example

### Input

```
PM2.5 = 85
PM10 = 120
```

### Output

```
AQI = 178
Category = Moderate
```

---

# Purpose

This project demonstrates how **environmental monitoring systems convert raw sensor readings into a standardized air quality index** that can be easily interpreted by users, governments, and decision-making systems.

---

# Project Structure

```
AQI-Calculator/
│
├── aqi_calculator.py
└── README.md
```

---

# Technologies Used

* Python
* Environmental Data Processing
* AQI Calculation (CPCB Standard)
