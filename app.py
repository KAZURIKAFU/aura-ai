"""
AuraAI — Intelligent Personal Assistant
Author: Abhay Sharma | github.com/KAZURIKAFU
LLM-powered conversational assistant with memory & tools
"""

import dash
from dash import dcc, html, Input, Output, State, ctx
import json
from datetime import datetime
from llm_engine import AuraEngine

# ── App ───────────────────────────────────────────────────────────────────────
app = dash.Dash(__name__, title="AuraAI | Abhay Sharma",
                meta_tags=[{"name":"viewport","content":"width=device-width,initial-scale=1"}],
                suppress_callback_exceptions=True)

C = {"bg":"#0d1117","card":"#161b22","card2":"#1c2128","card3":"#21262d",
     "blue":"#58a6ff","green":"#3fb950","orange":"#f78166","yellow":"#e3b341",
     "purple":"#bc8cff","text":"#e6edf3","sub":"#8b949e","border":"#30363d",
     "user_bubble":"#1f6feb","ai_bubble":"#161b22"}

ENGINE = AuraEngine()

QUICK_ACTIONS = [
    ("🤖", "Who are you?",                    "Who are you?"),
    ("🔢", "Calculate 25 * 48 + 100",          "Calculate 25 * 48 + 100"),
    ("🐍", "Write code for fibonacci",         "Write code for fibonacci"),
    ("📧", "Write email about project update", "Write email about project update"),
    ("📖", "What is machine learning?",        "What is machine learning?"),
    ("🛡️", "What is a DDoS attack?",           "What is a DDoS attack?"),
    ("☁️", "What is BigQuery?",                "What is BigQuery?"),
    ("🤖", "What is Generative AI?",           "What is Generative AI?"),
    ("📊", "What is MLOps?",                   "What is MLOps?"),
    ("🔐", "What is SQL Injection?",           "What is SQL Injection?"),
]

# ── Layout ────────────────────────────────────────────────────────────────────
app.layout = html.Div(style={"backgroundColor":C["bg"],"height":"100vh","display":"flex",
                              "flexDirection":"column","fontFamily":"'Segoe UI',Arial,sans-serif",
                              "color":C["text"],"overflow":"hidden"}, children=[

    # ── Header ──
    html.Div(style={"background":"linear-gradient(135deg,#0d1117,#1a1f35,#0d2137)",
                    "padding":"14px 28px","borderBottom":f"1px solid {C['border']}",
                    "flexShrink":"0","boxShadow":"0 2px 20px rgba(88,166,255,0.1)"}, children=[
        html.Div(style={"display":"flex","justifyContent":"space-between","alignItems":"center"}, children=[
            html.Div(style={"display":"flex","alignItems":"center","gap":"12px"}, children=[
                html.Div(style={"width":"40px","height":"40px","borderRadius":"50%",
                                "background":"linear-gradient(135deg,#58a6ff,#bc8cff)",
                                "display":"flex","alignItems":"center","justifyContent":"center",
                                "fontSize":"20px"}, children="🤖"),
                html.Div(children=[
                    html.H1("AuraAI", style={"margin":"0","fontSize":"20px","fontWeight":"700",
                                              "color":"#ffffff"}),
                    html.P("Intelligent Personal Assistant · NLP · Memory · Tools",
                           style={"margin":"0","fontSize":"10px","color":C["blue"]}),
                ])
            ]),
            html.Div(style={"display":"flex","gap":"8px","alignItems":"center"}, children=[
                html.Span("💬 NLP Engine",    style={"backgroundColor":"rgba(88,166,255,0.1)",
                                                      "color":C["blue"],"padding":"3px 10px",
                                                      "borderRadius":"20px","fontSize":"10px",
                                                      "border":f"1px solid {C['blue']}"}),
                html.Span("🧠 Memory",        style={"backgroundColor":"rgba(188,140,255,0.1)",
                                                      "color":C["purple"],"padding":"3px 10px",
                                                      "borderRadius":"20px","fontSize":"10px",
                                                      "border":f"1px solid {C['purple']}"}),
                html.Span("🔧 Tools",         style={"backgroundColor":"rgba(63,185,80,0.1)",
                                                      "color":C["green"],"padding":"3px 10px",
                                                      "borderRadius":"20px","fontSize":"10px",
                                                      "border":f"1px solid {C['green']}"}),
                html.Div(style={"fontSize":"11px","color":C["sub"]}, children=[
                    html.Span("By "),
                    html.Span("Abhay Sharma", style={"color":C["blue"],"fontWeight":"600"}),
                ]),
            ]),
        ])
    ]),

    # ── Main Body ──
    html.Div(style={"display":"flex","flex":"1","overflow":"hidden"}, children=[

        # ── Sidebar ──
        html.Div(style={"width":"260px","backgroundColor":C["card"],"borderRight":f"1px solid {C['border']}",
                        "padding":"16px","display":"flex","flexDirection":"column",
                        "gap":"12px","overflowY":"auto","flexShrink":"0"}, children=[

            # Stats
            html.Div(id="stats-panel", style={"backgroundColor":C["card2"],"borderRadius":"10px",
                                               "padding":"14px","border":f"1px solid {C['border']}"}),

            html.Hr(style={"border":f"1px solid {C['border']}","margin":"0"}),

            # Quick Actions
            html.H3("⚡ Quick Actions", style={"margin":"0","fontSize":"12px","color":C["sub"],
                                                "textTransform":"uppercase","letterSpacing":"1px"}),
            html.Div(children=[
                html.Button(f"{icon} {label[:28]}",
                            id={"type":"quick-action","index":i},
                            n_clicks=0,
                            style={"width":"100%","textAlign":"left","backgroundColor":C["card2"],
                                   "color":C["sub"],"border":f"1px solid {C['border']}",
                                   "borderRadius":"6px","padding":"7px 10px","fontSize":"11px",
                                   "cursor":"pointer","marginBottom":"4px","lineHeight":"1.4"})
                for i,(icon,label,_) in enumerate(QUICK_ACTIONS)
            ]),

            html.Hr(style={"border":f"1px solid {C['border']}","margin":"0"}),

            # Capabilities
            html.H3("🛠️ Capabilities", style={"margin":"0","fontSize":"12px","color":C["sub"],
                                                "textTransform":"uppercase","letterSpacing":"1px"}),
            html.Div(children=[
                html.Div(style={"padding":"6px 8px","marginBottom":"4px","borderRadius":"6px",
                                "backgroundColor":C["card2"],"border":f"1px solid {C['border']}",
                                "fontSize":"11px","color":C["sub"]}, children=cap)
                for cap in ["💬 Natural language Q&A","🔢 Math calculations",
                             "🐍 Python code generation","📧 Email drafting",
                             "📝 Text summarization","🧠 Conversation memory",
                             "☁️ Cloud & AI knowledge","🔐 Cybersecurity Q&A"]
            ]),

            html.Hr(style={"border":f"1px solid {C['border']}","margin":"0"}),

            # Clear button
            html.Button("🗑️ Clear Conversation", id="clear-btn", n_clicks=0,
                        style={"width":"100%","backgroundColor":"rgba(247,129,102,0.1)",
                               "color":C["orange"],"border":f"1px solid {C['orange']}",
                               "borderRadius":"6px","padding":"8px","fontSize":"11px",
                               "cursor":"pointer","fontWeight":"600"}),

            # Author
            html.Div(style={"backgroundColor":C["card2"],"borderRadius":"8px","padding":"10px",
                             "border":f"1px solid {C['border']}"}, children=[
                html.P("👨‍💻 Abhay Sharma", style={"margin":"0 0 2px 0","fontSize":"11px",
                                                   "fontWeight":"600","color":C["text"]}),
                html.P("github.com/KAZURIKAFU", style={"margin":"0","fontSize":"10px","color":C["blue"]}),
            ]),
        ]),

        # ── Chat Area ──
        html.Div(style={"flex":"1","display":"flex","flexDirection":"column","overflow":"hidden"}, children=[

            # Messages
            html.Div(id="chat-messages",
                     style={"flex":"1","overflowY":"auto","padding":"20px 24px",
                             "display":"flex","flexDirection":"column","gap":"16px"}),

            # Input Area
            html.Div(style={"padding":"16px 24px","borderTop":f"1px solid {C['border']}",
                             "backgroundColor":C["card"],"flexShrink":"0"}, children=[
                html.Div(style={"display":"flex","gap":"10px","alignItems":"flex-end"}, children=[
                    dcc.Textarea(id="user-input",
                                 placeholder="Ask me anything... (Press Enter or click Send)",
                                 style={"flex":"1","backgroundColor":C["card2"],
                                        "border":f"1px solid {C['border']}","borderRadius":"10px",
                                        "padding":"12px 14px","color":C["text"],"fontSize":"14px",
                                        "outline":"none","resize":"none","minHeight":"44px",
                                        "maxHeight":"120px","lineHeight":"1.5","fontFamily":"inherit"},
                                 rows=1),
                    html.Button("Send ➤", id="send-btn", n_clicks=0,
                                style={"backgroundColor":C["blue"],"color":"#0d1117","border":"none",
                                       "borderRadius":"10px","padding":"12px 20px","fontSize":"14px",
                                       "fontWeight":"700","cursor":"pointer","flexShrink":"0",
                                       "height":"44px"}),
                ]),
                html.P("💡 Try: 'What is Gemini AI?' · 'Calculate 144 / 12' · 'Write code for sorting' · 'Write email about internship'",
                       style={"margin":"8px 0 0 0","fontSize":"10px","color":C["sub"]}),
            ]),
        ]),
    ]),

    # Stores
    dcc.Store(id="conversation-store", data=[]),
    dcc.Store(id="trigger-store", data=""),
])


# ── Helper: Render message bubble ────────────────────────────────────────────
def render_message(role: str, text: str, timestamp: str) -> html.Div:
    is_user = role == "user"
    return html.Div(
        style={"display":"flex","flexDirection":"row-reverse" if is_user else "row",
               "alignItems":"flex-start","gap":"10px"},
        children=[
            html.Div(style={"width":"32px","height":"32px","borderRadius":"50%","flexShrink":"0",
                             "background":("linear-gradient(135deg,#1f6feb,#58a6ff)" if is_user
                                           else "linear-gradient(135deg,#58a6ff,#bc8cff)"),
                             "display":"flex","alignItems":"center","justifyContent":"center",
                             "fontSize":"16px"},
                     children="👤" if is_user else "🤖"),
            html.Div(style={"maxWidth":"70%"}, children=[
                html.Div(style={"backgroundColor":C["user_bubble"] if is_user else C["card2"],
                                "borderRadius":"12px" if is_user else "12px",
                                "padding":"12px 16px",
                                "border":f"1px solid {'#1f6feb' if is_user else C['border']}"},
                         children=html.Div(
                             # Render markdown-style bold and code
                             [html.Span(text)],
                             style={"fontSize":"13px","lineHeight":"1.6","color":C["text"],
                                    "whiteSpace":"pre-wrap","fontFamily":"inherit"}
                         )),
                html.P(timestamp, style={"margin":"3px 6px 0 6px","fontSize":"9px","color":C["sub"],
                                          "textAlign":"right" if is_user else "left"}),
            ])
        ]
    )


def render_welcome() -> html.Div:
    return html.Div(style={"textAlign":"center","padding":"40px 20px"}, children=[
        html.Div(style={"width":"70px","height":"70px","borderRadius":"50%","margin":"0 auto 16px",
                        "background":"linear-gradient(135deg,#58a6ff,#bc8cff)",
                        "display":"flex","alignItems":"center","justifyContent":"center",
                        "fontSize":"32px"}, children="🤖"),
        html.H2("Hello! I'm AuraAI 👋",
                style={"margin":"0 0 8px 0","fontSize":"22px","color":C["text"]}),
        html.P("Your intelligent personal assistant powered by NLP & conversation memory.",
               style={"margin":"0 0 20px 0","fontSize":"13px","color":C["sub"]}),
        html.Div(style={"display":"flex","justifyContent":"center","gap":"10px","flexWrap":"wrap"}, children=[
            html.Div(style={"backgroundColor":C["card2"],"border":f"1px solid {C['border']}",
                             "borderRadius":"8px","padding":"12px 16px","width":"130px"}, children=[
                html.P(icon, style={"margin":"0 0 4px 0","fontSize":"22px"}),
                html.P(label, style={"margin":"0","fontSize":"11px","color":C["sub"]}),
            ]) for icon,label in [("💬","Ask Anything"),("🔢","Calculate"),
                                   ("🐍","Write Code"),("📧","Draft Email"),
                                   ("🧠","Remember Context"),("📝","Summarize")]
        ]),
        html.P("👈 Click a Quick Action or type below to get started!",
               style={"margin":"20px 0 0 0","fontSize":"12px","color":C["sub"],"fontStyle":"italic"}),
    ])


# ── Callback: Quick actions fill input ───────────────────────────────────────
@app.callback(
    Output("user-input","value"),
    Input({"type":"quick-action","index":dash.ALL},"n_clicks"),
    prevent_initial_call=True
)
def fill_quick_action(clicks):
    triggered = ctx.triggered_id
    if isinstance(triggered, dict):
        idx = triggered["index"]
        return QUICK_ACTIONS[idx][2]
    return ""


# ── Callback: Send message ────────────────────────────────────────────────────
@app.callback(
    Output("chat-messages","children"),
    Output("conversation-store","data"),
    Output("stats-panel","children"),
    Output("user-input","value", allow_duplicate=True),
    Input("send-btn","n_clicks"),
    Input("clear-btn","n_clicks"),
    State("user-input","value"),
    State("conversation-store","data"),
    prevent_initial_call=True
)
def handle_message(send_clicks, clear_clicks, user_text, conversation):
    triggered = ctx.triggered_id
    conversation = conversation or []

    # Clear
    if triggered == "clear-btn":
        ENGINE.memory.clear()
        stats = _render_stats(0)
        return [render_welcome()], [], stats, ""

    # Send
    if not user_text or not user_text.strip():
        return dash.no_update, conversation, dash.no_update, ""

    ts = datetime.now().strftime("%H:%M")

    # Get AI response
    result = ENGINE.respond(user_text.strip())
    ai_text = result["response"]

    # Add to conversation
    conversation.append({"role":"user",    "text":user_text.strip(), "ts":ts})
    conversation.append({"role":"assistant","text":ai_text,           "ts":ts})

    # Render messages
    messages = [render_welcome()] if not conversation else []
    for msg in conversation:
        messages.append(render_message(msg["role"], msg["text"], msg["ts"]))

    stats = _render_stats(len([m for m in conversation if m["role"]=="user"]))
    return messages, conversation, stats, ""


def _render_stats(turns: int) -> list:
    mem_stats = ENGINE.memory.get_stats()
    items = [
        ("💬 Turns",   str(turns)),
        ("🧠 Memory",  f"{mem_stats['window_size']}/{mem_stats['max_turns']}"),
        ("⏱️ Session", datetime.now().strftime("%H:%M")),
    ]
    return [
        html.H3("📊 Session Stats", style={"margin":"0 0 10px 0","fontSize":"12px",
                                            "color":C["sub"],"textTransform":"uppercase",
                                            "letterSpacing":"1px"}),
        *[html.Div(style={"display":"flex","justifyContent":"space-between",
                           "marginBottom":"6px"}, children=[
            html.Span(label, style={"fontSize":"11px","color":C["sub"]}),
            html.Span(value, style={"fontSize":"11px","color":C["text"],"fontWeight":"600"}),
        ]) for label,value in items]
    ]


# ── Initial render ────────────────────────────────────────────────────────────
@app.callback(
    Output("chat-messages","children", allow_duplicate=True),
    Output("stats-panel","children", allow_duplicate=True),
    Input("conversation-store","data"),
    prevent_initial_call="initial_call"
)
def init_chat(conv):
    return [render_welcome()], _render_stats(0)


if __name__ == "__main__":
    print("\n🤖 AuraAI Starting...")
    print("🌐 Open: http://localhost:8053\n")
    app.run(debug=False, port=8053)
