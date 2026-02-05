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
    ## MVP Investment Breakdown
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Core Equipment
    """)
    return


@app.cell
def _():
    ### Default upfront percentages for each item:
    PROJECTOR_UPFNT = 0
    ENCLOSURE_UPFNT = 100
    COMPUTER_UPFNT = 24
    LAUNCH_MON_UPFNT = 37
    return ENCLOSURE_UPFNT, LAUNCH_MON_UPFNT, PROJECTOR_UPFNT


@app.cell
def _(PROJECTOR_UPFNT, mo):
    # Projector
    projector_cost = mo.ui.number(start=0, stop=5000, value=1000, step=1, label="Cost ($)")
    projector_upfront_pct = mo.ui.slider(start=0, stop=100, value=PROJECTOR_UPFNT, step=1, label="Upfront %", show_value=True)
    projector_months = mo.ui.slider(start=0, stop=36, value=12, step=3, label="Months", show_value=True)
    projector_apr = mo.ui.slider(start=0, stop=20, value=0, step=0.5, label="APR %", show_value=True)

    mo.md("**Projector**"), mo.hstack([projector_cost, projector_upfront_pct, projector_months, projector_apr],
                                      justify="start")
    return (
        projector_apr,
        projector_cost,
        projector_months,
        projector_upfront_pct,
    )


@app.cell
def _(LAUNCH_MON_UPFNT, mo):
    # Launch Monitor
    launch_monitor_cost = mo.ui.number(start=0, stop=5000, value=2400, step=1, label="Cost ($)")
    launch_monitor_upfront_pct = mo.ui.slider(start=0, stop=100, value=LAUNCH_MON_UPFNT, step=1, label="Upfront %", show_value=True)
    launch_monitor_months = mo.ui.slider(start=0, stop=36, value=6, step=3, label="Months", show_value=True)
    launch_monitor_apr = mo.ui.slider(start=0, stop=20, value=5, step=0.5, label="APR %", show_value=True)

    mo.md("**Launch Monitor**"), mo.hstack(
        [launch_monitor_cost, launch_monitor_upfront_pct, launch_monitor_months, launch_monitor_apr], justify="start")
    return (
        launch_monitor_apr,
        launch_monitor_cost,
        launch_monitor_months,
        launch_monitor_upfront_pct,
    )


@app.cell
def _(ENCLOSURE_UPFNT, mo):
    # Enclosure
    enclosure_cost = mo.ui.number(start=0, stop=5000, value=2000, step=1, label="Cost ($)")
    enclosure_upfront_pct = mo.ui.slider(start=0, stop=100, value=ENCLOSURE_UPFNT, step=1, label="Upfront %", show_value=True)
    enclosure_months = mo.ui.slider(start=0, stop=36, value=12, step=3, label="Months", show_value=True)
    enclosure_apr = mo.ui.slider(start=0, stop=20, value=0, step=0.5, label="APR %", show_value=True)

    mo.md("**Inflatable Enclosure**"), mo.hstack(
        [enclosure_cost, enclosure_upfront_pct, enclosure_months, enclosure_apr], justify="start")
    return (
        enclosure_apr,
        enclosure_cost,
        enclosure_months,
        enclosure_upfront_pct,
    )


@app.cell
def _(mo):
    # Hitting Mat
    mat_cost = mo.ui.number(start=0, stop=2000, value=500, step=1, label="Cost ($)")
    mat_upfront_pct = mo.ui.slider(start=0, stop=100, value=100, step=1, label="Upfront %", show_value=True)
    mat_months = mo.ui.slider(start=0, stop=36, value=0, step=3, label="Months", show_value=True)
    mat_apr = mo.ui.slider(start=0, stop=20, value=0, step=0.5, label="APR %", show_value=True)

    mo.md("**Hitting Mat**"), mo.hstack([mat_cost, mat_upfront_pct, mat_months, mat_apr], justify="start")
    return mat_apr, mat_cost, mat_months, mat_upfront_pct


@app.cell
def _(mo):
    mo.md("""
    ### Supporting Equipment & Setup
    """)
    return


@app.cell
def _(mo):
    # Screen
    screen_cost = mo.ui.number(start=0, stop=1000, value=300, step=1, label="Cost ($)")
    screen_upfront_pct = mo.ui.slider(start=0, stop=100, value=100, step=1, label="Upfront %", show_value=True)
    screen_months = mo.ui.slider(start=0, stop=36, value=0, step=3, label="Months", show_value=True)
    screen_apr = mo.ui.slider(start=0, stop=20, value=0, step=0.5, label="APR %", show_value=True)

    mo.md("**Impact Screen**"), mo.hstack([screen_cost, screen_upfront_pct, screen_months, screen_apr], justify="start")
    return screen_apr, screen_cost, screen_months, screen_upfront_pct


@app.cell
def _(mo):
    # Computer/Tablet
    computer_cost = mo.ui.number(start=0, stop=2000, value=956, step=1, label="Cost ($)")
    computer_upfront_pct = mo.ui.slider(start=0, stop=100, value=24, step=1, label="Upfront %", show_value=True)
    computer_months = mo.ui.slider(start=0, stop=36, value=1.5, step=.5
                                   , label="Months", show_value=True)
    computer_apr = mo.ui.slider(start=0, stop=20, value=0, step=0.5, label="APR %", show_value=True)

    mo.md("**Computer/Tablet**"), mo.hstack([computer_cost, computer_upfront_pct, computer_months, computer_apr],
                                            justify="start")
    return computer_apr, computer_cost, computer_months, computer_upfront_pct


@app.cell
def _(mo):
    # Miscellaneous
    misc_cost = mo.ui.number(start=0, stop=2000, value=500, step=1, label="Cost ($)")
    misc_upfront_pct = mo.ui.slider(start=0, stop=100, value=100, step=1, label="Upfront %", show_value=True)
    misc_months = mo.ui.slider(start=0, stop=36, value=0, step=3, label="Months", show_value=True)
    misc_apr = mo.ui.slider(start=0, stop=20, value=0, step=0.5, label="APR %", show_value=True)

    mo.md("**Misc Equipment (cables, mounts, etc.)**"), mo.hstack([misc_cost, misc_upfront_pct, misc_months, misc_apr],
                                                                  justify="start")
    return misc_apr, misc_cost, misc_months, misc_upfront_pct


@app.cell
def _(
    computer_apr,
    computer_cost,
    computer_months,
    computer_upfront_pct,
    enclosure_apr,
    enclosure_cost,
    enclosure_months,
    enclosure_upfront_pct,
    launch_monitor_apr,
    launch_monitor_cost,
    launch_monitor_months,
    launch_monitor_upfront_pct,
    mat_apr,
    mat_cost,
    mat_months,
    mat_upfront_pct,
    misc_apr,
    misc_cost,
    misc_months,
    misc_upfront_pct,
    pd,
    projector_apr,
    projector_cost,
    projector_months,
    projector_upfront_pct,
    screen_apr,
    screen_cost,
    screen_months,
    screen_upfront_pct,
):
    # Compile all line items
    line_items_data = [
        {
            'item': 'Projector',
            'cost': projector_cost.value,
            'upfront_pct': projector_upfront_pct.value,
            'months': projector_months.value,
            'apr': projector_apr.value
        },
        {
            'item': 'Launch Monitor',
            'cost': launch_monitor_cost.value,
            'upfront_pct': launch_monitor_upfront_pct.value,
            'months': launch_monitor_months.value,
            'apr': launch_monitor_apr.value
        },
        {
            'item': 'Enclosure',
            'cost': enclosure_cost.value,
            'upfront_pct': enclosure_upfront_pct.value,
            'months': enclosure_months.value,
            'apr': enclosure_apr.value
        },
        {
            'item': 'Hitting Mat',
            'cost': mat_cost.value,
            'upfront_pct': mat_upfront_pct.value,
            'months': mat_months.value,
            'apr': mat_apr.value
        },
        {
            'item': 'Impact Screen',
            'cost': screen_cost.value,
            'upfront_pct': screen_upfront_pct.value,
            'months': screen_months.value,
            'apr': screen_apr.value
        },
        {
            'item': 'Computer/Tablet',
            'cost': computer_cost.value,
            'upfront_pct': computer_upfront_pct.value,
            'months': computer_months.value,
            'apr': computer_apr.value
        },
        {
            'item': 'Misc Equipment',
            'cost': misc_cost.value,
            'upfront_pct': misc_upfront_pct.value,
            'months': misc_months.value,
            'apr': misc_apr.value
        }
    ]

    # Calculate financing for each item
    def calculate_monthly_payment(principal, months, apr):
        """Calculate monthly payment with interest"""
        if months == 0 or principal == 0:
            return 0

        monthly_rate = (apr / 100) / 12

        if monthly_rate == 0:
            return principal / months
        else:
            return principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)

    # Process each line item
    for _item in line_items_data:
        _item['upfront_payment'] = _item['cost'] * (_item['upfront_pct'] / 100)
        _item['financed_amount'] = _item['cost'] - _item['upfront_payment']
        _item['monthly_payment'] = calculate_monthly_payment(
            _item['financed_amount'],
            _item['months'],
            _item['apr']
        )

    df_line_items = pd.DataFrame(line_items_data)

    # Calculate total investment metrics
    total_investment_amount = df_line_items['cost'].sum()
    total_upfront_payment = df_line_items['upfront_payment'].sum()
    total_financed = df_line_items['financed_amount'].sum()
    return (
        df_line_items,
        total_financed,
        total_investment_amount,
        total_upfront_payment,
    )


@app.cell
def _(mo, total_financed, total_investment_amount, total_upfront_payment):
    # Display investment summary
    investment_summary_html = f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 12px; color: white; margin: 20px 0;">
        <h3 style="margin-top: 0;">Investment Summary</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 15px;">
            <div>
                <div style="font-size: 14px; opacity: 0.9;">Total Investment</div>
                <div style="font-size: 28px; font-weight: bold;">${total_investment_amount:,.0f}</div>
            </div>
            <div>
                <div style="font-size: 14px; opacity: 0.9;">Upfront Payment</div>
                <div style="font-size: 28px; font-weight: bold;">${total_upfront_payment:,.0f}</div>
            </div>
            <div>
                <div style="font-size: 14px; opacity: 0.9;">Total Financed</div>
                <div style="font-size: 28px; font-weight: bold;">${total_financed:,.0f}</div>
            </div>
        </div>
    </div>
    """

    mo.Html(investment_summary_html)
    return


@app.cell
def _(df_line_items, mo):
    # Display line items table
    mo.md("### Line Items Breakdown")

    display_items = df_line_items[
        ['item', 'cost', 'upfront_payment', 'financed_amount', 'months', 'apr', 'monthly_payment']].copy()
    display_items.columns = ['Item', 'Cost', 'Upfront', 'Financed', 'Months', 'APR %', 'Monthly Payment']
    display_items['Cost'] = display_items['Cost'].apply(lambda x: f"${x:,.0f}")
    display_items['Upfront'] = display_items['Upfront'].apply(lambda x: f"${x:,.0f}")
    display_items['Financed'] = display_items['Financed'].apply(lambda x: f"${x:,.0f}")
    display_items['Monthly Payment'] = display_items['Monthly Payment'].apply(lambda x: f"${x:,.0f}")
    display_items['APR %'] = display_items['APR %'].apply(lambda x: f"{x:.1f}%")

    mo.ui.table(display_items)
    return


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
        value=75,
        step=5,
        label="Weekday Hourly Rate ($)"
    )

    weekend_hourly_rate = mo.ui.number(
        start=50,
        stop=400,
        value=100,
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
        value=.5,
        step=0.5,
        label="Weekday Bookings per Week",
        show_value=True
    )

    weekend_bookings_per_week = mo.ui.slider(
        start=0,
        stop=4,
        value=.5,
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
        value=3,
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
        stop=1000,
        value=75,
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
    avg_weekday_hours,
    avg_weekend_hours,
    cost_per_booking,
    df_line_items,
    monthly_insurance,
    monthly_maintenance,
    monthly_storage,
    other_monthly_costs,
    pd,
    total_upfront_payment,
    weekday_bookings_per_week,
    weekday_hourly_rate,
    weekend_bookings_per_week,
    weekend_hourly_rate,
):
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

    # Calculate operating margin
    monthly_operating_margin = monthly_revenue - total_monthly_operating_costs

    # Build monthly financing schedule - each item has its own payment schedule
    months = 24

    # Create payment schedule for each item
    payment_schedules = []

    for _, _item in df_line_items.iterrows():
        if _item['months'] > 0:
            schedule = {
                'item': _item['item'],
                'monthly_payment': _item['monthly_payment'],
                'end_month': int(_item['months'])
            }
            payment_schedules.append(schedule)

    # Build monthly projections
    cash_flows = []
    cumulative_profit = -total_upfront_payment  # Start with upfront payment as negative

    STARTUP_MONTHS = 2
    for month in range(1, months + 1):
        # Calculate total financing payment for this month
        total_financing_payment = 0
        active_items = []

        for schedule in payment_schedules:
            if month <= schedule['end_month']:
                total_financing_payment += schedule['monthly_payment']
                active_items.append(schedule['item'])

        if month > STARTUP_MONTHS:
            monthly_rev_for_loop = monthly_revenue # assume normal revenue in the startup months
            net_cash_flow = monthly_operating_margin - total_financing_payment
            cumulative_profit += net_cash_flow
        
        elif month <= STARTUP_MONTHS:
            monthly_rev_for_loop = 0
            net_cash_flow = -total_financing_payment
            cumulative_profit += 0 # assume zero-revenue in the startup months


        cash_flows.append({
            'Month': month,
            'Revenue': monthly_rev_for_loop, # allows for us to set revenue = 0 in startup months
            'Operating Costs': total_monthly_operating_costs,
            'Financing Payment': total_financing_payment,
            'Active Financed Items': len(active_items),
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
        payback_month = ">24"
    return (
        df_projections,
        fixed_costs,
        monthly_operating_margin,
        monthly_revenue,
        payback_month,
        total_monthly_operating_costs,
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
    fixed_costs,
    mo,
    monthly_operating_margin,
    monthly_revenue,
    payback_month,
    total_monthly_operating_costs,
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
            <div style="font-size: 12px; opacity: 0.9; margin-top: 5px;">{(monthly_operating_margin/monthly_revenue*100) if monthly_revenue > 0 else 0:.1f}% margin</div>
        </div>
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 10px; color: white;">
            <div style="font-size: 14px; opacity: 0.9;">Payback Period</div>
            <div style="font-size: 32px; font-weight: bold;">{payback_month} mo</div>
        </div>
    </div>

    <div style="background: #e5e7eb; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #d1d5db;">
        <h3 style="margin-top: 0; color: #1f2937;">Cost Structure</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; color: #374151;">
            <div>
                <strong style="color: #111827;">Variable Costs:</strong> ${variable_costs:,.0f}/mo
            </div>
            <div>
                <strong style="color: #111827;">Fixed Costs:</strong> ${fixed_costs:,.0f}/mo
            </div>
            <div>
                <strong style="color: #111827;">Total Operating Costs:</strong> ${total_monthly_operating_costs:,.0f}/mo
            </div>
            <div>
                <strong style="color: #111827;">Operating Margin:</strong> {(monthly_operating_margin/monthly_revenue*100) if monthly_revenue > 0 else 0:.1f}%
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
        line=dict(color='#f59e0b', width=2, dash='dash'),
        fill='tozeroy',
        fillcolor='rgba(245, 158, 11, 0.1)'
    ))

    fig_cashflow.add_trace(go.Scatter(
        x=df_projections['Month'],
        y=df_projections['Net Cash Flow'],
        name='Net Cash Flow',
        mode='lines',
        line=dict(color='#6366f1', width=3)
    ))

    fig_cashflow.update_layout(
        title='Monthly Cash Flow Analysis - Financing Payments Decline as Items Are Paid Off',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        height=450,
        template='plotly_white'
    )

    fig_cashflow
    return


@app.cell
def _(df_projections, go):
    # Create cumulative profit chart
    fig_cumulative = go.Figure()

    # Color the line based on positive/negative
    colors = ['#ef4444' if x < 0 else '#10b981' for x in df_projections['Cumulative Profit']]

    fig_cumulative.add_trace(go.Scatter(
        x=df_projections['Month'],
        y=df_projections['Cumulative Profit'],
        name='Cumulative Profit',
        mode='lines',
        fill='tozeroy',
        line=dict(color='#8b5cf6', width=3),
        fillcolor='rgba(139, 92, 246, 0.2)'
    ))

    # Add break-even line
    fig_cumulative.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray",
        line_width=2,
        annotation_text="Break-even",
        annotation_position="right"
    )

    fig_cumulative.update_layout(
        title='Cumulative Profit Over Time',
        xaxis_title='Month',
        yaxis_title='Cumulative Profit ($)',
        hovermode='x unified',
        height=450,
        template='plotly_white'
    )

    fig_cumulative
    return


@app.cell
def _(df_projections, go):
    # Create financing payment waterfall chart
    fig_financing = go.Figure()

    fig_financing.add_trace(go.Bar(
        x=df_projections['Month'],
        y=df_projections['Financing Payment'],
        name='Total Financing Payment',
        marker=dict(
            color=df_projections['Financing Payment'],
            colorscale='Oranges',
            showscale=False
        )
    ))

    fig_financing.update_layout(
        title='Monthly Financing Payments - Shows When Each Item Is Paid Off',
        xaxis_title='Month',
        yaxis_title='Financing Payment ($)',
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )

    fig_financing
    return


@app.cell
def _(mo):
    mo.md(f"""
    ## Detailed Monthly Projections

    First 12 months shown below. Notice how financing payments change as individual items are paid off.
    """)
    return


@app.cell
def _(df_projections, mo):
    # Display table with first 12 months
    display_df_proj = df_projections.head(12).copy()
    display_df_proj['Revenue'] = display_df_proj['Revenue'].apply(lambda x: f"${x:,.0f}")
    display_df_proj['Operating Costs'] = display_df_proj['Operating Costs'].apply(lambda x: f"${x:,.0f}")
    display_df_proj['Financing Payment'] = display_df_proj['Financing Payment'].apply(lambda x: f"${x:,.0f}")
    display_df_proj['Net Cash Flow'] = display_df_proj['Net Cash Flow'].apply(lambda x: f"${x:,.0f}")
    display_df_proj['Cumulative Profit'] = display_df_proj['Cumulative Profit'].apply(lambda x: f"${x:,.0f}")

    mo.ui.table(display_df_proj[['Month', 'Revenue', 'Operating Costs', 'Financing Payment', 'Active Financed Items',
                                 'Net Cash Flow', 'Cumulative Profit']])
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    ## Quick Quote Generator

    Use this to quickly generate quotes for potential clients based on your pricing model.
    """)
    return


@app.cell
def _(mo):
    quote_hours = mo.ui.slider(
        start=2,
        stop=8,
        value=3,
        step=0.5,
        label="Event Duration (hours)",
        show_value=True
    )

    quote_is_weekend = mo.ui.checkbox(label="Weekend Event?", value=False)

    mo.hstack([quote_hours, quote_is_weekend], justify="start")
    return quote_hours, quote_is_weekend


@app.cell
def _(
    cost_per_booking,
    mo,
    quote_hours,
    quote_is_weekend,
    weekday_hourly_rate,
    weekend_hourly_rate,
):
    # Calculate quote
    rate = weekend_hourly_rate.value if quote_is_weekend.value else weekday_hourly_rate.value
    quote_total = rate * quote_hours.value
    quote_cost = cost_per_booking.value
    quote_margin = quote_total - quote_cost
    quote_margin_pct = (quote_margin / quote_total * 100) if quote_total > 0 else 0

    quote_html = f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 12px; color: white; margin: 20px 0;">
        <h3 style="margin-top: 0;">Quote Summary</h3>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 20px;">
            <div>
                <div style="font-size: 14px; opacity: 0.9;">Event Type</div>
                <div style="font-size: 24px; font-weight: bold;">{"Weekend" if quote_is_weekend.value else "Weekday"}</div>
            </div>
            <div>
                <div style="font-size: 14px; opacity: 0.9;">Hourly Rate</div>
                <div style="font-size: 24px; font-weight: bold;">${rate:,.0f}/hr</div>
            </div>
            <div>
                <div style="font-size: 14px; opacity: 0.9;">Total Quote</div>
                <div style="font-size: 32px; font-weight: bold;">${quote_total:,.0f}</div>
            </div>
            <div>
                <div style="font-size: 14px; opacity: 0.9;">Your Margin</div>
                <div style="font-size: 32px; font-weight: bold;">${quote_margin:,.0f}</div>
                <div style="font-size: 12px; opacity: 0.9; margin-top: 5px;">{quote_margin_pct:.1f}% margin</div>
            </div>
        </div>
    </div>
    """

    mo.Html(quote_html)
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    ### Tips for Using This Model

    - **Line Items**: Each equipment purchase has its own financing terms - adjust them independently
    - **Financing Payments**: Watch the financing payment chart to see when each item is paid off
    - **Pricing Strategy**: Use the quote generator to quickly price events for clients
    - **Utilization**: Be conservative early on - it's better to exceed low expectations
    - **Break-even Focus**: Aim for payback within 12-18 months for healthy business

    **Next Steps**:
    - Export to HTML for static deployment: `marimo export html golf_simulator_model_v2.py -o index.html`
    - Share with partners for input on assumptions
    - Update as you get actual quotes and financing terms from vendors
    """)
    return


if __name__ == "__main__":
    app.run()
