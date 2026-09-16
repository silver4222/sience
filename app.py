import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="반응 시간 측정 실험",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ 반응 시간 측정 실험")

st.write(
    "정보 전달 방식을 선택한 후 시작 버튼을 누르세요. "
    "신호가 나타나면 최대한 빠르게 스페이스바를 누릅니다."
)

st.divider()

# -----------------------------------------
# 실험 조건 선택
# -----------------------------------------

condition = st.radio(
    "실험 조건을 선택하세요.",
    [
        "💡 빛만",
        "🔊 소리만",
        "💡🔊 빛 + 소리"
    ],
    horizontal=False
)

st.divider()

st.info(
    "시작 버튼을 누르면 2~5초 사이의 랜덤한 시간이 지난 후 "
    "신호가 나타납니다."
)

# -----------------------------------------
# 실험 시작
# -----------------------------------------

if st.button("🚀 시작", use_container_width=True):

    if condition == "💡 빛만":
        mode = "visual"

    elif condition == "🔊 소리만":
        mode = "audio"

    else:
        mode = "both"

    # JavaScript를 이용한 반응시간 측정
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">

        <style>
            body {{
                margin: 0;
                padding: 0;
                text-align: center;
                font-family: Arial, sans-serif;
                background: transparent;
            }}

            #box {{
                width: 250px;
                height: 250px;
                margin: 30px auto;
                border-radius: 20px;
                border: 3px solid #cccccc;
                background: white;

                display: flex;
                align-items: center;
                justify-content: center;

                font-size: 30px;
                font-weight: bold;

                transition: background 0.05s;
            }}

            #message {{
                font-size: 20px;
                margin-top: 15px;
            }}

            #result {{
                font-size: 32px;
                font-weight: bold;
                margin-top: 20px;
            }}
        </style>
    </head>

    <body>

        <div id="box">준비</div>

        <div id="message">
            시작되었습니다.<br>
            신호가 나타날 때까지 기다리세요.
        </div>

        <div id="result"></div>


        <script>

            const mode = "{mode}";

            const box = document.getElementById("box");
            const message = document.getElementById("message");
            const result = document.getElementById("result");

            let startTime = null;
            let finished = false;


            // --------------------------------
            // 2~5초 랜덤 대기
            // --------------------------------

            const delay =
                Math.floor(Math.random() * 3000) + 2000;


            setTimeout(function() {{

                if (finished) return;

                // 반응시간 측정 시작
                startTime = performance.now();


                // --------------------------------
                // 빛
                // --------------------------------

                if (mode === "visual" || mode === "both") {{

                    box.style.background = "black";
                    box.style.color = "white";
                    box.innerText = "⚡";

                }}


                // --------------------------------
                // 소리
                // --------------------------------

                if (mode === "audio" || mode === "both") {{

                    try {{

                        const AudioContext =
                            window.AudioContext ||
                            window.webkitAudioContext;

                        const audioContext =
                            new AudioContext();

                        const oscillator =
                            audioContext.createOscillator();

                        const gain =
                            audioContext.createGain();


                        oscillator.type = "sine";

                        oscillator.frequency.value = 1000;

                        gain.gain.value = 0.25;


                        oscillator.connect(gain);

                        gain.connect(
                            audioContext.destination
                        );


                        oscillator.start();

                        oscillator.stop(
                            audioContext.currentTime + 0.15
                        );

                    }} catch (error) {{

                        console.log(error);

                    }}

                }}


                message.innerHTML =
                    "⚡ 신호 발생!<br>" +
                    "<b>지금 스페이스바를 누르세요!</b>";

            }}, delay);


            // --------------------------------
            // 스페이스바 감지
            // --------------------------------

            document.addEventListener(
                "keydown",
                function(event) {{

                    if (event.code !== "Space") {{
                        return;
                    }}

                    event.preventDefault();


                    // 신호가 나오기 전에 누른 경우
                    if (startTime === null) {{

                        message.innerHTML =
                            "❌ 너무 빨리 눌렀습니다.<br>" +
                            "다시 시작해주세요.";

                        finished = true;

                        return;
                    }}


                    // 이미 측정이 끝난 경우
                    if (finished) {{
                        return;
                    }}


                    finished = true;


                    // 반응시간 계산
                    const reactionTime =
                        performance.now() - startTime;


                    const milliseconds =
                        reactionTime.toFixed(2);


                    // 화면 표시
                    box.style.background = "#eeeeee";
                    box.style.color = "black";
                    box.innerText = "✓";


                    message.innerHTML =
                        "측정 완료!";


                    result.innerHTML =
                        milliseconds + " ms";


                    // 복사하기 쉽게 텍스트 표시
                    result.setAttribute(
                        "data-time",
                        milliseconds
                    );

                }}
            );

        </script>

    </body>
    </html>
    """

    components.html(
        html,
        height=420
    )

    st.success(
        "위 실험 화면에서 결과가 표시되면 "
        "그 시간을 실험 기록표에 적어주세요."
    )

st.divider()

st.caption(
    "예: 0.285초 → 285 ms로 기록하면 됩니다."
)
