import marimo

__generated_with = "0.19.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    return go, mo, pd


@app.cell
def _(mo):
    mo.md("""
    # Golf Simulator Business Financial Model

    Build your pricing strategy and analyze profitability for your mobile golf simulator rental business.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Initial Investment & Financing
    """)
    return


@app.cell
def _(mo):
    # Investment parameters
    total_investment = mo.ui.number(
        start=0,
        stop=20000,
        value=6500,
        step=1,
        label="Total Investment ($)"
    )

    upfront_percentage = mo.ui.slider(
        start=0,
        stop=100,
        value=20,
        step=1,
        label="Upfront Payment (%)",
        show_value=True
    )

    financing_months = mo.ui.slider(
        start=3,
        stop=36,
        value=12,
        step=3,
        label="Financing Term (months)",
        show_value=True
    )

    annual_interest_rate = mo.ui.slider(
        start=0,
        stop=15,
        value=0,
        step=0.5,
        label="Annual Interest Rate (%)",
        show_value=True
    )

    mo.hstack([
        mo.vstack([total_investment, upfront_percentage]),
        mo.vstack([financing_months, annual_interest_rate])
    ], justify="space-around")
    return (
        annual_interest_rate,
        financing_months,
        total_investment,
        upfront_percentage,
    )


@app.cell
def _(mo):
    mo.md("""
    ## Pricing Strategy
    """)
    return


@app.cell
def _(mo):
    # Pricing parameters
    weekday_hourly_rate = mo.ui.number(
        start=50,
        stop=300,
        value=125,
        step=5,
        label="Weekday Hourly Rate ($)"
    )

    weekend_hourly_rate = mo.ui.number(
        start=50,
        stop=400,
        value=175,
        step=5,
        label="Weekend Hourly Rate ($)"
    )

    min_booking_hours = mo.ui.number(
        start=1,
        stop=6,
        value=2,
        step=1,
        label="Minimum Booking (hours)"
    )

    mo.hstack([weekday_hourly_rate, weekend_hourly_rate, min_booking_hours], justify="space-around")
    return weekday_hourly_rate, weekend_hourly_rate


@app.cell
def _(mo):
    mo.md("""
    ## Utilization Assumptions
    """)
    return


@app.cell
def _(mo):
    # Utilization parameters
    weekday_bookings_per_week = mo.ui.slider(
        start=0,
        stop=5,
        value=2,
        step=0.5,
        label="Weekday Bookings per Week",
        show_value=True
    )

    weekend_bookings_per_week = mo.ui.slider(
        start=0,
        stop=4,
        value=2,
        step=0.5,
        label="Weekend Bookings per Week",
        show_value=True
    )

    avg_weekday_hours = mo.ui.slider(
        start=2,
        stop=8,
        value=3,
        step=0.5,
        label="Avg Weekday Booking Length (hours)",
        show_value=True
    )

    avg_weekend_hours = mo.ui.slider(
        start=2,
        stop=8,
        value=4,
        step=0.5,
        label="Avg Weekend Booking Length (hours)",
        show_value=True
    )

    mo.hstack([
        mo.vstack([weekday_bookings_per_week, weekend_bookings_per_week]),
        mo.vstack([avg_weekday_hours, avg_weekend_hours])
    ], justify="space-around")
    return (
        avg_weekday_hours,
        avg_weekend_hours,
        weekday_bookings_per_week,
        weekend_bookings_per_week,
    )


@app.cell
def _(mo):
    mo.md("""
    ## Operating Costs
    """)
    return


@app.cell
def _(mo):
    # Operating costs
    cost_per_booking = mo.ui.number(
        start=0,
        stop=100,
        value=25,
        step=5,
        label="Variable Cost per Booking ($)",
        full_width=False
    )

    monthly_insurance = mo.ui.number(
        start=0,
        stop=500,
        value=100,
        step=25,
        label="Monthly Insurance ($)",
        full_width=False
    )

    monthly_maintenance = mo.ui.number(
        start=0,
        stop=300,
        value=50,
        step=10,
        label="Monthly Maintenance ($)",
        full_width=False
    )

    monthly_storage = mo.ui.number(
        start=0,
        stop=500,
        value=0,
        step=25,
        label="Monthly Storage ($)",
        full_width=False
    )

    other_monthly_costs = mo.ui.number(
        start=0,
        stop=500,
        value=50,
        step=10,
        label="Other Monthly Costs ($)",
        full_width=False
    )

    mo.hstack([
        mo.vstack([cost_per_booking, monthly_insurance]),
        mo.vstack([monthly_maintenance, monthly_storage]),
        mo.vstack([other_monthly_costs])
    ], justify="space-around")
    return (
        cost_per_booking,
        monthly_insurance,
        monthly_maintenance,
        monthly_storage,
        other_monthly_costs,
    )


@app.cell
def _(
    annual_interest_rate,
    avg_weekday_hours,
    avg_weekend_hours,
    cost_per_booking,
    financing_months,
    monthly_insurance,
    monthly_maintenance,
    monthly_storage,
    other_monthly_costs,
    pd,
    total_investment,
    upfront_percentage,
    weekday_bookings_per_week,
    weekday_hourly_rate,
    weekend_bookings_per_week,
    weekend_hourly_rate,
):
    # Calculate financing details
    upfront_payment = total_investment.value * (upfront_percentage.value / 100)
    financed_amount = total_investment.value - upfront_payment
    monthly_rate = (annual_interest_rate.value / 100) / 12

    # Calculate monthly payment (simple installment with interest)
    if monthly_rate > 0:
        monthly_payment = financed_amount * (monthly_rate * (1 + monthly_rate) ** financing_months.value) / \
                          ((1 + monthly_rate) ** financing_months.value - 1)
    else:
        monthly_payment = financed_amount / financing_months.value if financing_months.value > 0 else 0

    # Calculate monthly revenue
    weekly_weekday_revenue = weekday_bookings_per_week.value * avg_weekday_hours.value * weekday_hourly_rate.value
    weekly_weekend_revenue = weekend_bookings_per_week.value * avg_weekend_hours.value * weekend_hourly_rate.value
    monthly_revenue = (weekly_weekday_revenue + weekly_weekend_revenue) * 4.33  # avg weeks per month

    # Calculate monthly costs
    total_bookings_per_month = (weekday_bookings_per_week.value + weekend_bookings_per_week.value) * 4.33
    variable_costs = total_bookings_per_month * cost_per_booking.value
    fixed_costs = (monthly_insurance.value + monthly_maintenance.value +
                   monthly_storage.value + other_monthly_costs.value)
    total_monthly_operating_costs = variable_costs + fixed_costs

    # Calculate metrics
    monthly_operating_margin = monthly_revenue - total_monthly_operating_costs

    # Build monthly projections
    months = 36  # 3 year projection
    cash_flows = []
    cumulative_profit = -upfront_payment  # Start with upfront payment as negative

    for month in range(1, months + 1):
        # Payment only during financing period
        payment = monthly_payment if month <= financing_months.value else 0

        net_cash_flow = monthly_operating_margin - payment
        cumulative_profit += net_cash_flow

        cash_flows.append({
            'Month': month,
            'Revenue': monthly_revenue,
            'Operating Costs': total_monthly_operating_costs,
            'Financing Payment': payment,
            'Net Cash Flow': net_cash_flow,
            'Cumulative Profit': cumulative_profit
        })

    df_projections = pd.DataFrame(cash_flows)

    # Calculate payback period
    payback_month = None
    for idx, row in df_projections.iterrows():
        if row['Cumulative Profit'] >= 0:
            payback_month = row['Month']
            break

    if payback_month is None:
        payback_month = ">36"
    return (
        df_projections,
        financed_amount,
        fixed_costs,
        monthly_operating_margin,
        monthly_payment,
        monthly_revenue,
        payback_month,
        total_monthly_operating_costs,
        upfront_payment,
        variable_costs,
    )


@app.cell
def _(mo):
    mo.md("""
    ## Financial Summary
    """)
    return


@app.cell
def _(
    financed_amount,
    fixed_costs,
    mo,
    monthly_operating_margin,
    monthly_payment,
    monthly_revenue,
    payback_month,
    total_monthly_operating_costs,
    upfront_payment,
    variable_costs,
):
    # Display key metrics
    metrics_html = f"""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white;">
            <div style="font-size: 14px; opacity: 0.9;">Monthly Revenue</div>
            <div style="font-size: 32px; font-weight: bold;">${monthly_revenue:,.0f}</div>
        </div>
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 10px; color: white;">
            <div style="font-size: 14px; opacity: 0.9;">Monthly Operating Margin</div>
            <div style="font-size: 32px; font-weight: bold;">${monthly_operating_margin:,.0f}</div>
            <div style="font-size: 12px; opacity: 0.9; margin-top: 5px;">{(monthly_operating_margin / monthly_revenue * 100) if monthly_revenue > 0 else 0:.1f}% margin</div>
        </div>
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 10px; color: white;">
            <div style="font-size: 14px; opacity: 0.9;">Payback Period</div>
            <div style="font-size: 32px; font-weight: bold;">{payback_month} mo</div>
        </div>
    </div>

    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h3 style="margin-top: 0;">Investment Breakdown</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div>
                <strong>Upfront Payment:</strong> ${upfront_payment:,.0f}
            </div>
            <div>
                <strong>Financed Amount:</strong> ${financed_amount:,.0f}
            </div>
            <div>
                <strong>Monthly Payment:</strong> ${monthly_payment:,.0f}
            </div>
            <div>
                <strong>Payment Duration:</strong> Until paid off
            </div>
        </div>
    </div>

    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h3 style="margin-top: 0;">Cost Structure</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div>
                <strong>Variable Costs:</strong> ${variable_costs:,.0f}/mo
            </div>
            <div>
                <strong>Fixed Costs:</strong> ${fixed_costs:,.0f}/mo
            </div>
            <div>
                <strong>Total Operating Costs:</strong> ${total_monthly_operating_costs:,.0f}/mo
            </div>
            <div>
                <strong>Operating Margin:</strong> {(monthly_operating_margin / monthly_revenue * 100) if monthly_revenue > 0 else 0:.1f}%
            </div>
        </div>
    </div>
    """

    mo.Html(metrics_html)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Cash Flow Projections
    """)
    return


@app.cell
def _(df_projections, go):
    # Create cash flow chart
    fig_cashflow = go.Figure()

    fig_cashflow.add_trace(go.Scatter(
        x=df_projections['Month'],
        y=df_projections['Revenue'],
        name='Revenue',
        mode='lines',
        line=dict(color='#10b981', width=2)
    ))

    fig_cashflow.add_trace(go.Scatter(
        x=df_projections['Month'],
        y=df_projections['Operating Costs'],
        name='Operating Costs',
        mode='lines',
        line=dict(color='#ef4444', width=2)
    ))

    fig_cashflow.add_trace(go.Scatter(
        x=df_projections['Month'],
        y=df_projections['Financing Payment'],
        name='Financing Payment',
        mode='lines',
        line=dict(color='#f59e0b', width=2, dash='dash')
    ))

    fig_cashflow.add_trace(go.Scatter(
        x=df_projections['Month'],
        y=df_projections['Net Cash Flow'],
        name='Net Cash Flow',
        mode='lines',
        line=dict(color='#6366f1', width=3)
    ))

    fig_cashflow.update_layout(
        title='Monthly Cash Flow Analysis',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )

    fig_cashflow
    return


@app.cell
def _(df_projections, go):
    # Create cumulative profit chart
    fig_cumulative = go.Figure()

    fig_cumulative.add_trace(go.Scatter(
        x=df_projections['Month'],
        y=df_projections['Cumulative Profit'],
        name='Cumulative Profit',
        mode='lines',
        fill='tozeroy',
        line=dict(color='#8b5cf6', width=3)
    ))

    # Add break-even line
    fig_cumulative.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray",
        annotation_text="Break-even",
        annotation_position="right"
    )

    fig_cumulative.update_layout(
        title='Cumulative Profit Over Time',
        xaxis_title='Month',
        yaxis_title='Cumulative Profit ($)',
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )

    fig_cumulative
    return


@app.cell
def _(mo):
    mo.md(f"""
    ## Detailed Monthly Projections

    First 12 months shown below. Full dataset available for export.
    """)
    return


@app.cell
def _(df_projections, mo):
    # Display table with first 12 months
    display_df = df_projections.head(12).copy()
    display_df['Revenue'] = display_df['Revenue'].apply(lambda x: f"${x:,.0f}")
    display_df['Operating Costs'] = display_df['Operating Costs'].apply(lambda x: f"${x:,.0f}")
    display_df['Financing Payment'] = display_df['Financing Payment'].apply(lambda x: f"${x:,.0f}")
    display_df['Net Cash Flow'] = display_df['Net Cash Flow'].apply(lambda x: f"${x:,.0f}")
    display_df['Cumulative Profit'] = display_df['Cumulative Profit'].apply(lambda x: f"${x:,.0f}")

    mo.ui.table(display_df)
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    ### Tips for Using This Model

    - **Pricing Strategy**: Adjust weekday vs weekend rates to optimize revenue
    - **Utilization**: Be realistic about booking frequency, especially in early months
    - **Operating Costs**: Don't forget gas, tolls, setup time, and wear & tear
    - **Scenario Analysis**: Try conservative, moderate, and aggressive scenarios
    - **Break-even Focus**: Aim for payback within 12-18 months for healthy business

    **Next Steps**: Export this to HTML and share with your partners, or run locally to iterate on assumptions.
    """)
    return


if __name__ == "__main__":
    app.run()
