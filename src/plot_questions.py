import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def s6q1(popular_articles, popular_conferences):
    print('='*32)
    print('\tPOPULAR ARTICLES')
    print('-'*32)
    print(popular_articles.head(5))
    print('='*32)
    print('='*20)
    print('ARTICLES ANALYSIS')
    print('-'*20)
    print(popular_articles.describe(include=["int64"]))
    print('='*20)
    print('='*20)
    print('POPULAR CONFERENCES')
    print('-'*20)
    print(popular_conferences.head(5))
    print('='*20)
    print('='*20)
    print('CONFERENCES ANALYSIS')
    print('-'*20)
    print(popular_conferences.describe(include=["int64"]))
    print('='*20)
    popular_articles = popular_articles.sort_values("papers", ascending=False)

    mp_articles = popular_articles[:10].copy()
    mp_articles.loc[10] = ["Other", popular_articles[10:]["papers"].sum()]
    mp_articles = mp_articles.sort_values("papers", ascending=False)

    BG = "#0d1117"
    FONT = "DM Mono, IBM Plex Mono, monospace"

    fig = px.pie(
        mp_articles,
        names="venue",
        values="papers",
        hole=0.55,
        title="Top Publication Venues in Industry",
        color_discrete_sequence=px.colors.sequential.Tealgrn
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Papers: %{value}<br>Share: %{percent}<extra></extra>",
        marker=dict(line=dict(color=BG, width=2))
    )

    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(color="#c9d1d9", family=FONT),
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(size=18, color="#e6edf3", family=FONT)
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
        margin=dict(t=80, b=40, l=40, r=40),
        height=450,
    )

    fig.show()
    BG   = "#0d1117"
    FONT = "DM Mono, IBM Plex Mono, monospace"

    data = mp_articles.sort_values("papers")[0:10]
    fig = px.bar(
        data,
        x="papers",
        y="venue",
        orientation="h",
        title="Top-10 Publication Venues",
        color="papers",
        color_continuous_scale="Tealgrn"
    )

    fig.update_traces(
        text=data["papers"],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Papers: %{x}<extra></extra>",
        marker=dict(line=dict(color=BG, width=1.5))
    )

    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(color="#c9d1d9", family=FONT),
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(size=18, color="#e6edf3", family=FONT)
        ),
        xaxis=dict(
            title="Number of Papers",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            zeroline=False
        ),
        yaxis=dict(
            title="",
            showgrid=False
        ),
        coloraxis_showscale=False,
        margin=dict(t=80, b=40, l=120, r=40),
        height=450
    )
    fig.update_xaxes(range=[0, data["papers"].max() * 1.15])
    fig.show()
    popular_conferences = popular_conferences.sort_values("papers", ascending=False)

    mp_conf = popular_conferences[:10].copy()
    mp_conf.loc[10] = ["Other", popular_conferences[10:]["papers"].sum()]
    mp_conf = mp_conf.sort_values("papers", ascending=False)

    BG = "#0d1117"
    FONT = "DM Mono, IBM Plex Mono, monospace"

    fig = px.pie(
        mp_conf,
        names="venue",
        values="papers",
        hole=0.55,
        title="Top Conferences in the Industry",
        color_discrete_sequence=px.colors.sequential.Tealgrn
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Papers: %{value}<br>Share: %{percent}<extra></extra>",
        marker=dict(line=dict(color=BG, width=2))
    )

    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(color="#c9d1d9", family=FONT),
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(size=18, color="#e6edf3", family=FONT)
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        ),
        margin=dict(t=80, b=40, l=40, r=40),
        height=450,
    )

    fig.show()
    BG   = "#0d1117"
    FONT = "DM Mono, IBM Plex Mono, monospace"

    data = mp_conf[1:].sort_values("papers")

    fig = px.bar(
        data,
        x="papers",
        y="venue",
        orientation="h",
        title="Top-10 Conferences",
        color="papers",
        color_continuous_scale="Tealgrn"
    )

    fig.update_traces(
        text=data["papers"],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Papers: %{x}<extra></extra>",
        marker=dict(line=dict(color=BG, width=1.5))
    )

    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(color="#c9d1d9", family=FONT),
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(size=18, color="#e6edf3", family=FONT)
        ),
        xaxis=dict(
            title="Number of Papers",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            zeroline=False
        ),
        yaxis=dict(
            title="",
            showgrid=False
        ),
        coloraxis_showscale=False,
        margin=dict(t=80, b=40, l=140, r=80),
        height=450
    )

    fig.update_xaxes(range=[0, data["papers"].max() * 1.15])

    fig.show()


def s6q2(ai_citations):
    print('='*72)
    print('\t\t\tOVERVIEW OF CATEGORIES')
    print('-'*72)
    print(ai_citations)
    print('='*72)
    print('='*48)
    print('\t\tCATEGORIES ANALYSIS')
    print('-'*48)
    print(ai_citations.describe())
    print('='*48)
    BG   = "#0d1117"
    FONT = "DM Mono, IBM Plex Mono, monospace"

    fig = px.pie(
        ai_citations,
        names="category",
        values="paperCount",
        hole=0.55,
        title="Paper Count per Category",
        color_discrete_sequence=px.colors.sequential.Tealgrn
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Papers: %{value}<br>Share: %{percent}<extra></extra>",
        marker=dict(line=dict(color=BG, width=2))
    )

    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(color="#c9d1d9", family=FONT),
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(size=18, color="#e6edf3", family=FONT)
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11)
        ),
        margin=dict(t=80, b=40, l=40, r=40),
        height=450
    )

    fig.show()
    BG   = "#0d1117"
    FONT = "DM Mono, IBM Plex Mono, monospace"

    fig = px.pie(
        ai_citations,
        names="category",
        values="totalCitations",
        hole=0.55,
        title="Citations per Category",
        color_discrete_sequence=px.colors.sequential.Tealgrn
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Citations: %{value}<br>Share: %{percent}<extra></extra>",
        marker=dict(line=dict(color=BG, width=2))
    )

    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(color="#c9d1d9", family=FONT),
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(size=18, color="#e6edf3", family=FONT)
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11)
        ),
        margin=dict(t=80, b=40, l=40, r=40),
        height=450
    )

    fig.show()
    BG   = "#0d1117"
    FONT = "DM Mono, IBM Plex Mono, monospace"

    fig = go.Figure(data=[
        go.Bar(
            name="Citations",
            x=ai_citations.category,
            y=ai_citations.totalCitations,
            marker=dict(color="#FF6B6B", line=dict(color=BG, width=1.5)),
            hovertemplate="<b>%{x}</b><br>Citations: %{y}<extra></extra>"
        ),
        go.Bar(
            name="Papers",
            x=ai_citations.category,
            y=ai_citations.paperCount,
            marker=dict(color="#4ECDC4", line=dict(color=BG, width=1.5)),
            hovertemplate="<b>%{x}</b><br>Papers: %{y}<extra></extra>"
        )
    ])

    fig.update_layout(
        barmode="group",
        title=dict(
            text="Citations & Papers per Category",
            x=0.5,
            xanchor="center",
            font=dict(size=18, color="#e6edf3", family=FONT)
        ),
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(color="#c9d1d9", family=FONT),
        xaxis=dict(
            title="",
            showgrid=False,
            tickangle=-20
        ),
        yaxis=dict(
            title="Count",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            zeroline=False
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            y=1.08,
            x=0.5,
            xanchor="center"
        ),
        margin=dict(t=90, b=80, l=60, r=40),
        height=450
    )

    fig.show()
    ai_citations['citPerPaper'] = (
        ai_citations.totalCitations / ai_citations.paperCount)
    BG   = "#0d1117"
    FONT = "DM Mono, IBM Plex Mono, monospace"

    fig = px.bar(
        ai_citations,
        x="category",
        y="citPerPaper",
        color="citPerPaper",
        title="Citations per Paper by Category",
        color_continuous_scale="Tealgrn"
    )

    fig.update_traces(
        text=ai_citations["citPerPaper"].round(2),
        textposition="outside",
        marker=dict(line=dict(color=BG, width=1.5)),
        hovertemplate="<b>%{x}</b><br>Citations per Paper: %{y:.2f}<extra></extra>"
    )

    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(color="#c9d1d9", family=FONT),
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(size=18, color="#e6edf3", family=FONT)
        ),
        xaxis=dict(
            title="",
            tickangle=-20,
            showgrid=False
        ),
        yaxis=dict(
            title="Citations per Paper",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            zeroline=False
        ),
        coloraxis_showscale=False,
        margin=dict(t=60, b=80, l=60, r=40),
        height=450
    )

    fig.show()
    print('='*35)
    print('  CITATIONS PER PAPER ANALYSIS')
    print('-'*35)
    print(ai_citations.citPerPaper.describe())
    print('='*35)


def cumulate_vol_avg(df1, df2, df3):
    volume1 = df1.totalVolume
    volume2 = df2.totalVolume
    volume3 = df3.totalVolume
    ttl_vol = volume1 + volume2 + volume3
    ratio1 = volume1 / ttl_vol
    ratio2 = volume2 / ttl_vol
    ratio3 = volume3 / ttl_vol
    avg_year = (df1.avgYear * ratio1 + df2.avgYear * ratio2 
                + df3.avgYear * ratio3)
    return ttl_vol, avg_year


def s7q1(df_before2011, df_from2021onwards, df_2011to2021, funap_df):
    df_before2011.sort_values('subtopic', inplace=True, ignore_index=True)
    df_from2021onwards.sort_values('subtopic', inplace=True, ignore_index=True)
    df_2011to2021.sort_values('subtopic', inplace=True, ignore_index=True)
    volume, average_year = cumulate_vol_avg(df_from2021onwards,
                                            df_before2011, df_2011to2021)

    evolution = df_before2011.iloc[:, :2]
    evolution['avgYear'] = average_year
    evolution['totalVolume'] = volume

    print('='*65)
    print('\t\t\tEVOLUTION OF TOPICS')
    print('-'*65)
    print(evolution)
    print('='*65)
    print('='*47)
    print('\t  ANALYSIS OF EVOLUTION')
    print('-'*47)
    print(evolution.describe())
    print('='*47)

    dates = evolution.birthYear + np.array([0,0,0.7,0,0.7,0,0,0])
    labels = evolution.subtopic

    x_stem = np.array([2.0 if i%2==0 else -2.0 for i in range(len(dates))])
    x_label = x_stem.copy()

    for i, l in enumerate(labels):
        if l == 'Ethics & Interpretability':
            x_label[i] = -2

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[0,0],
        y=[min(dates)-5, max(dates)+5],
        mode='lines',
        line=dict(color='deeppink', width=3),
        showlegend=False
    ))

    for xi, yi, xs in zip(x_stem, dates, x_stem):
        if int(yi) == 1993.0:
            fig.add_trace(go.Scatter(
                x=[-xi, xi],
                y=[yi, yi],
                mode='lines',
                line=dict(color='darkmagenta', width=2),
                showlegend=False
            ))
        fig.add_trace(go.Scatter(
            x=[0, xi],
            y=[yi, yi],
            mode='lines',
            line=dict(color='darkmagenta', width=2),
            showlegend=False
        ))

    fig.add_trace(go.Scatter(
        x=np.zeros(len(dates)),
        y=dates,
        mode='markers',
        marker=dict(size=12, color='palevioletred'),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=np.zeros(len(dates)),
        y=dates,
        mode='markers',
        marker=dict(size=6, color='darkmagenta'),
        showlegend=False
    ))

    for xi, yi, label in zip(x_label, dates, labels):
        fig.add_trace(go.Scatter(
            x=[xi],
            y=[yi+0.5],
            mode='text',
            text=[f"{label}, {int(yi)}"],
            textposition='middle right' if xi < 0 else 'middle left',
            textfont=dict(family='serif', size=12, color='royalblue'),
            showlegend=False
        ))

    fig.update_layout(
        title=dict(text='Important Milestones in AI', x=0.5,
                    font=dict(family='serif', size=16, color='royalblue')),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='#0f1117',
        paper_bgcolor='#0f1117',
        margin=dict(t=80, l=20, r=20, b=20),
        height=700,
    )

    fig.show()

    fig = px.bar(
            evolution, x='birthYear', y='subtopic', orientation='h',
            base='birthYear', color='totalVolume', range_x=[1945, 2026],
            title='Subtopic birth year and volume comparison up to 2026',
            custom_data=['birthYear', 'totalVolume']
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Birth year: %{customdata[0]}<br>"
            "Total volume: %{customdata[1]}<br>"
            "<extra></extra>"
        ),
        marker=dict(line=dict(color='#0f1117', width=1))
    )

    fig.update_layout(
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        font=dict(family="IBM Plex Mono, monospace", color="#c9d1d9", size=12),
        xaxis=dict(
            title="Total Volume",
            gridcolor="#21262d",
            linecolor="#30363d",
            zeroline=False,
            tickcolor="#30363d"
        ),
        yaxis=dict(
            title="Subtopic",
            gridcolor="#21262d",
            linecolor="#30363d",
            tickcolor="#30363d",
            autorange="reversed"
        ),
        title=dict(
            x=0.04,
            font=dict(size=18, color="#e6edf3")
        ),
        coloraxis_showscale=False,
        margin=dict(t=60, r=30, b=60, l=120),
    )

    fig.show()

    evolution['volPerYear'] = (evolution.totalVolume / (2026 - evolution.birthYear)).astype('int64')

    fig = px.bar(
        evolution,
        x='volPerYear',
        y='subtopic',
        orientation='h',
        color='volPerYear',
        title='Subtopic Volume per Year',
        custom_data=['volPerYear'],
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Volume per year: %{customdata[0]}<br>"
            "<extra></extra>"
        ),
        marker=dict(line=dict(color='#0f1117', width=1))
    )

    fig.update_layout(
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        font=dict(family="IBM Plex Mono, monospace", color="#c9d1d9", size=12),
        xaxis=dict(
            title="Volume per Year",
            gridcolor="#21262d",
            linecolor="#30363d",
            zeroline=False,
            tickcolor="#30363d"
        ),
        yaxis=dict(
            title="Subtopic",
            gridcolor="#21262d",
            linecolor="#30363d",
            tickcolor="#30363d",
            autorange="reversed"
        ),
        title=dict(
            x=0.04,
            font=dict(size=18, color="#e6edf3")
        ),
        coloraxis_showscale=False,
        margin=dict(t=60, r=30, b=60, l=120),
    )

    fig.show()

    print('='*32)
    print('\tVOLUME PER YEAR')
    print('-'*32)
    print(evolution.volPerYear.describe())
    print('='*32)

    fig = px.bar(
            evolution, x='avgYear', y='subtopic', orientation='h',
            base='avgYear', color='totalVolume', range_x=[2014, 2026],
            title='Subtopic average year (by paper) and volume comparison up to 2026',
            custom_data=['avgYear', 'totalVolume']
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Average year: %{customdata[0]}<br>"
            "Total volume: %{customdata[1]}<br>"
            "<extra></extra>"
        ),
        marker=dict(line=dict(color='#0f1117', width=1))
    )

    fig.update_layout(
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        font=dict(family="IBM Plex Mono, monospace", color="#c9d1d9", size=12),
        xaxis=dict(
            title="Total Volume",
            gridcolor="#21262d",
            linecolor="#30363d",
            zeroline=False,
            tickcolor="#30363d"
        ),
        yaxis=dict(
            title="Subtopic",
            gridcolor="#21262d",
            linecolor="#30363d",
            tickcolor="#30363d",
            autorange="reversed"
        ),
        title=dict(
            x=0.04,
            font=dict(size=18, color="#e6edf3")
        ),
        coloraxis_showscale=False,
        margin=dict(t=60, r=30, b=60, l=120),
    )

    fig.show()

    df_before2011['collectionYear'] = 2010
    df_2011to2021['collectionYear'] = 2021
    df_from2021onwards['collectionYear'] = 2026
    df_from2021onwards.birthYear = df_before2011.birthYear
    df_2011to2021.birthYear = df_before2011.birthYear

    PALETTE = ["#00C9A7", "#FF6B6B", "#8AACAA", "#FFE66D", "#A78BFA", "#F97316", "#00C43B", '#F20D5F']

    def build_traces(d1, d2, d3):
        all_data = pd.concat([d1, d2, d3], ignore_index=True)
        subtopics = all_data["subtopic"].unique()

        traces = []
        for i, sub in enumerate(subtopics):
            rows = all_data[all_data["subtopic"] == sub].sort_values("collectionYear")

            birth_year = rows["birthYear"].iloc[0]
            x = [birth_year] + rows["collectionYear"].tolist()
            y = [0] + rows["totalVolume"].cumsum().tolist()

            traces.append(go.Scatter(
                x=x,
                y=y,
                mode="lines+markers",
                name=sub,
                line=dict(color=PALETTE[i % len(PALETTE)], width=2.5, shape="spline"),
                marker=dict(size=7, symbol="circle"),
            ))

        return traces


    fig = go.Figure(data=build_traces(df_before2011, df_2011to2021, df_from2021onwards))

    fig.update_layout(
        title=dict(text="Volume by subtopic", x=0.04, font=dict(size=18, color="#e6edf3")),
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        font=dict(family="IBM Plex Mono, monospace", color="#c9d1d9", size=12),
        xaxis=dict(
            title="Year",
            gridcolor="#21262d",
            linecolor="#30363d",
            tickcolor="#30363d",
            zeroline=False,
            tickformat="d",
        ),
        yaxis=dict(
            title="Cumulative Volume",
            gridcolor="#21262d",
            linecolor="#30363d",
            tickcolor="#30363d",
            zeroline=True,
            zerolinecolor="#30363d",
        ),
        legend=dict(
            bgcolor="rgba(22,27,34,0.85)",
            bordercolor="#30363d",
            borderwidth=1,
            x=0.02, y=0.98,
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#161b22",
            bordercolor="#30363d",
            font=dict(family="IBM Plex Mono, monospace", size=12),
        ),
        margin=dict(t=60, r=30, b=60, l=70),
    )

    fig.show()

    evolution["gap"] = evolution["avgYear"].astype('int64') - evolution["birthYear"]
    df = evolution.sort_values("gap", ascending=True).reset_index(drop=True)

    COLOR_BIRTH = "#4ECDC4"
    COLOR_AVG   = "#FF6B6B"
    COLOR_LINE  = "rgba(255,255,255,0.12)"

    fig = go.Figure()

    for _, row in df.iterrows():
        fig.add_shape(
            type="line",
            x0=row["birthYear"], x1=row["avgYear"],
            y0=row["subtopic"],  y1=row["subtopic"],
            line=dict(color=COLOR_LINE, width=6),
            layer="below",
        )

    fig.add_trace(go.Scatter(
        x=df["birthYear"],
        y=df["subtopic"],
        mode="markers",
        name="Birth Year",
        marker=dict(color=COLOR_BIRTH, size=16, line=dict(color="#0f1117", width=2)),
        hovertemplate="<b>%{y}</b><br>Birth Year: %{x}<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=df["avgYear"],
        y=df["subtopic"],
        mode="markers",
        name="Avg Paper Year",
        marker=dict(color=COLOR_AVG, size=16, line=dict(color="#0f1117", width=2)),
        hovertemplate="<b>%{y}</b><br>Avg Paper Year: %{x}<br>Gap: %{customdata} yrs<extra></extra>",
        customdata=df["gap"],
    ))

    for _, row in df.iterrows():
        mid_x = (row["birthYear"] + row["avgYear"]) / 2
        fig.add_annotation(
            x=mid_x, y=row["subtopic"],
            text=f"+{row['gap']} yrs",
            showarrow=False,
            yshift=14,
            font=dict(size=10, color="rgba(200,200,200,0.6)", family="IBM Plex Mono, monospace"),
        )

    fig.update_layout(
        title=dict(
            text="Birth year to Average paper year by subtopic",
            x=0.04,
            font=dict(size=18, color="#e6edf3", family="IBM Plex Mono, monospace"),
        ),
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        font=dict(family="IBM Plex Mono, monospace", color="#c9d1d9", size=12),
        xaxis=dict(
            title="Year",
            gridcolor="#21262d",
            linecolor="#30363d",
            tickcolor="#30363d",
            zeroline=False,
            tickformat="d",
        ),
        yaxis=dict(
            gridcolor="#21262d",
            linecolor="#30363d",
            tickcolor="#30363d",
            tickfont=dict(size=13),
        ),
        legend=dict(
            bgcolor="rgba(22,27,34,0.85)",
            bordercolor="#30363d",
            borderwidth=1,
            orientation="h",
            x=0.5, xanchor="center",
            y=1.08,
        ),
        hovermode="y unified",
        margin=dict(t=80, r=40, b=60, l=100),
        height=120 + len(df) * 60,
    )

    fig.show()

    print('='*35)
    print('\t  FIELDS OVERVIEW')
    print('-'*35)
    print(funap_df)
    print('='*35)

    fig = px.pie(
        funap_df, 
        names='type', 
        values='count',
        title='Applied vs Fundamental Research by Paper Numbers',
        color_discrete_sequence=["#00C9A7", "#FF6B6B"],
    )


    fig.update_traces(
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>",
        marker=dict(line=dict(color='#0f1117', width=2))
    )

    fig.update_layout(
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        font=dict(family="IBM Plex Mono, monospace", color="#c9d1d9", size=12),
        title=dict(
            x=0.5,
            font=dict(size=18, color="#e6edf3")
        ),
        margin=dict(t=60, r=30, b=60, l=30),
    )

    fig.show()

    fund = funap_df[funap_df["type"] == "Fundamental"]["avgYear"].values[0]
    appl = funap_df[funap_df["type"] == "Applied"]["avgYear"].values[0]
    gap  = round(appl - fund, 2)
    mid  = (fund + appl) / 2

    COLOR_FUND  = "#4ECDC4"
    COLOR_APPL  = "#FF6B6B"
    BG          = "#0d1117"
    FONT        = "DM Mono, IBM Plex Mono, monospace"

    fig = go.Figure()

    steps = 60
    for i in range(steps):
        x0 = fund + (appl - fund) * (i / steps)
        x1 = fund + (appl - fund) * ((i + 1) / steps)
        r = int(0x4E + (0xFF - 0x4E) * (i / steps))
        g = int(0xCD + (0x6B - 0xCD) * (i / steps))
        b = int(0xC4 + (0x6B - 0xC4) * (i / steps))
        fig.add_shape(
            type="line",
            x0=x0, x1=x1, y0=0, y1=0,
            line=dict(color=f"rgb({r},{g},{b})", width=5),
            layer="below",
        )

    fig.add_shape(
        type="line",
        x0=fund, x1=appl, y0=0, y1=0,
        line=dict(color="rgba(255,255,255,0.04)", width=20),
        layer="below",
    )

    for x, color in [(fund, COLOR_FUND), (appl, COLOR_APPL)]:
        fig.add_shape(type="line",
            x0=x, x1=x, y0=-0.08, y1=0.08,
            line=dict(color=color, width=2),
        )

    fig.add_trace(go.Scatter(
        x=[fund, appl], y=[0, 0],
        mode="markers",
        marker=dict(
            color=[COLOR_FUND, COLOR_APPL],
            size=22,
            line=dict(color=BG, width=3),
        ),
        showlegend=False,
        hovertemplate="%{customdata}<br><b>%{x}</b><extra></extra>",
        customdata=["Fundamental", "Applied"],
    ))

    for x, label, color in [(fund, "FUNDAMENTAL", COLOR_FUND), (appl, "APPLIED", COLOR_APPL)]:
        fig.add_annotation(
            x=x, y=0,
            text=f"<b>{label}</b>",
            showarrow=False, yshift=38,
            font=dict(size=13, color=color, family=FONT),
        )
        fig.add_annotation(
            x=x, y=0,
            text=f"<b>{int(x)}</b>",
            showarrow=False, yshift=18,
            font=dict(size=22, color=color, family=FONT),
        )

    fig.add_annotation(
        x=mid, y=0,
        text=f"<b>+{gap} yrs</b>",
        showarrow=False, yshift=-36,
        font=dict(size=13, color="rgba(200,210,220,0.65)", family=FONT),
        bgcolor="rgba(255,255,255,0.04)",
        bordercolor="rgba(255,255,255,0.10)",
        borderwidth=1,
        borderpad=6,
    )

    fig.add_annotation(
        x=appl - (appl - fund) * 0.07, y=0,
        ax=fund + (appl - fund) * 0.07, ay=0,
        axref="x", ayref="y",
        showarrow=True,
        arrowhead=2, arrowsize=1.2,
        arrowwidth=1.5,
        arrowcolor="rgba(255,255,255,0.15)",
        text="",
    )

    fig.update_layout(
        title=dict(
            text=(
                "<b>Applied vs Fundamental Research</b>"
                "<br><sup>Average publication year comparison</sup>"
            ),
            x=0.5, xanchor="center",
            font=dict(size=16, color="#e6edf3", family=FONT),
        ),
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family=FONT, color="#c9d1d9"),
        xaxis=dict(
            showgrid=False, zeroline=False,
            showline=False, showticklabels=False,
            range=[fund-1, appl+1],
        ),
        yaxis=dict(
            showgrid=False, zeroline=False,
            showline=False, showticklabels=False,
            range=[-2, 2],
        ),
        margin=dict(t=100, b=80, l=60, r=60),
        height=280,
        width=700,
    )

    fig.show()