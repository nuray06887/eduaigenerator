""")
st.stop()

# ==================== ЗАГОЛОВОК ====================
st.markdown('<div class="main-title">🎓 УМНЫЙ ГЕНЕРАТОР ЛЕКЦИЙ И ИНТЕРАКТИВНЫХ ИГР</div>', unsafe_allow_html=True)

# ==================== ВКЛАДКИ ====================
tab1, tab2 = st.tabs(["📖 ГЕНЕРАТОР ЛЕКЦИЙ", "🎮 ИНТЕРАКТИВНЫЕ ИГРЫ"])

# ==================== ВКЛАДКА 1: ЛЕКЦИИ ====================
with tab1:
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">
            <span>🌟</span> Что вас интересует?
        </div>
    """, unsafe_allow_html=True)

    topic = st.text_input("", placeholder="Например: Квантовая физика, История Казахстана, Python для начинающих...", label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">
            <span>📖</span> РЕЗУЛЬТАТ
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 СГЕНЕРИРОВАТЬ ЛЕКЦИЮ", use_container_width=True):
        if not topic.strip():
            st.warning("⚠️ Введите тему лекции!")
        else:
            start_time = time.time()
            
            with st.status("Генерирую лекцию...", expanded=True) as status:
                st.write("🔍 Анализ темы...")
                st.write("📚 Сбор информации...")
                st.write("✍️ Написание лекции...")
                lecture, error = generate_lecture(topic)
                
                elapsed_time = time.time() - start_time
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                
                if error:
                    status.update(label="Ошибка!", state="error")
                    st.error(f"❌ {error}")
                else:
                    st.session_state.last_lecture = lecture
                    st.session_state.last_topic = topic
                    token_count = count_tokens(lecture)
                    status.update(label="✅ Лекция готова!", state="complete")
                    
                    if minutes > 0:
                        time_str = f"{minutes} мин {seconds} сек"
                    else:
                        time_str = f"{seconds} сек"
                    
                    st.success(f"✅ Лекция сгенерирована за **{time_str}**")
                    st.info(f"📊 Объём лекции: ~{token_count} токенов (~{token_count//4} слов)")

    if st.session_state.last_lecture:
        with st.expander("📖 Показать лекцию", expanded=True):
            st.markdown(st.session_state.last_lecture)

        st.download_button(
            "📥 Скачать лекцию (TXT)",
            st.session_state.last_lecture,
            file_name=f"lekciya_{st.session_state.last_topic[:30].replace(' ', '_')}.txt"
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== ВКЛАДКА 2: ИГРЫ ====================
with tab2:
st.markdown("""
<div class="card">
    <div class="card-title">
        <span>🎮</span> ИНТЕРАКТИВНЫЕ ИГРЫ И ЗАДАНИЯ
    </div>
""", unsafe_allow_html=True)

game_choice = st.selectbox(
    "🎲 Выберите тип активности:",
    ["📝 Викторина", "✅ Правда или ложь", "🃏 Найди пару", "💻 Практическое задание"]
)

col_game1, col_game2 = st.columns(2)
with col_game1:
    use_lecture_topic = st.checkbox(
        "Использовать тему из последней лекции",
        value=bool(st.session_state.last_topic)
    )

with col_game2:
    if use_lecture_topic and st.session_state.last_topic:
        st.info(f"🎯 Тема: **{st.session_state.last_topic}**")
        game_topic = st.session_state.last_topic
    else:
        game_topic = st.text_input(
            "📝 Введите тему:",
            placeholder="Например: HTML, создание веб-страницы"
        )

if game_choice != "💻 Практическое задание":
    num_questions = st.slider("🔢 Количество заданий:", 3, 10, 5)
else:
    st.info("📝 Будет сгенерировано **одно** практическое задание. Справа вы увидите, как должна выглядеть готовая страница.")

if st.button("🎮 НАЧАТЬ", use_container_width=True):
    actual_topic = game_topic.strip() if game_topic else ""
    if not actual_topic:
        st.warning("⚠️ Введите тему!")
    else:
        with st.spinner("🔄 Генерация..."):
            error = None

            if game_choice == "📝 Викторина":
                questions, error = generate_quiz(actual_topic, num_questions)
                if not error:
                    reset_game()
                    st.session_state.quiz_questions = questions
                    st.session_state.game_active = True
                    st.session_state.game_type = "quiz"
                    st.success(f"✅ Создано {len(questions)} вопросов!")
                    time.sleep(0.5)
                    st.rerun()

            elif game_choice == "✅ Правда или ложь":
                statements, error = generate_true_false(actual_topic, num_questions)
                if not error:
                    reset_game()
                    st.session_state.quiz_questions = statements
                    st.session_state.game_active = True
                    st.session_state.game_type = "truefalse"
                    st.success(f"✅ Создано {len(statements)} утверждений!")
                    time.sleep(0.5)
                    st.rerun()

            elif game_choice == "🃏 Найди пару":
                pairs, error = generate_match_pairs(actual_topic, num_questions)
                if not error:
                    reset_game()
                    defs = [p["definition"] for p in pairs]
                    random.shuffle(defs)
                    st.session_state.quiz_questions = pairs
                    st.session_state.shuffled_defs = defs
                    st.session_state.game_active = True
                    st.session_state.game_type = "match"
                    st.success(f"✅ Создано {len(pairs)} пар!")
                    time.sleep(0.5)
                    st.rerun()

            elif game_choice == "💻 Практическое задание":
                task, error = generate_practical_task(actual_topic, st.session_state.last_lecture if use_lecture_topic else None)
                if not error:
                    reset_game()
                    st.session_state.task_data = task
                    st.session_state.game_active = True
                    st.session_state.game_type = "task"
                    st.success(f"✅ Задание создано!")
                    time.sleep(0.5)
                    st.rerun()

            if error:
                st.error(f"❌ {error}")

st.markdown('</div>', unsafe_allow_html=True)

# ==================== АКТИВНАЯ ИГРА / ЗАДАНИЕ ====================
if st.session_state.game_active:
    st.markdown("---")
    st.markdown('<div class="game-card">', unsafe_allow_html=True)

    # ---------- ПРАКТИЧЕСКОЕ ЗАДАНИЕ ----------
    if st.session_state.game_type == "task" and st.session_state.task_data:
        task = st.session_state.task_data
        
        st.markdown("### 💻 ПРАКТИЧЕСКОЕ ЗАДАНИЕ")
        st.markdown(f"#### {task.get('title', 'Задание')}")
        st.markdown(task.get('description', ''))
        
        if task.get('code'):
            code = task.get('code', '')
            
            col_left, col_right = st.columns([1, 1])
            
            with col_left:
                st.markdown("**📝 Код с пропусками:**")
                st.markdown(f'<div class="task-code">{code}</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("**✏️ Вставьте пропущенные теги (через запятую):**")
                st.caption("Пример: h1, /h1, p, /p")
                
                user_answer = st.text_area(
                    "",
                    placeholder="Например: h1, /h1, p, /p",
                    height=80,
                    key="task_answer_input",
                    label_visibility="collapsed"
                )
                
                col_check, col_hint = st.columns(2)
                with col_check:
                    if st.button("✅ Проверить ответ", key="check_task"):
                        if user_answer.strip():
                            correct = task.get('correct_answer', '').lower().strip()
                            user = user_answer.strip().lower()
                            
                            correct_clean = re.sub(r'\s+', '', correct)
                            user_clean = re.sub(r'\s+', '', user)
                            
                            if correct_clean in user_clean or user_clean in correct_clean:
                                st.success("🎉 Правильно! Отличная работа!")
                                st.balloons()
                            else:
                                st.error(f"❌ Неправильно. Попробуйте ещё раз!")
                                st.info(f"💡 Подсказка: {task.get('hint', 'Подумайте ещё раз')}")
                        else:
                            st.warning("Введите ответ!")
                
                with col_hint:
                    if st.button("💡 Показать подсказку", key="show_hint"):
                        st.info(f"💡 {task.get('hint', 'Подсказка не предоставлена')}")
                
                if st.button("🔄 Новое задание", key="new_task"):
                    reset_game()
                    st.rerun()
            
            with col_right:
                st.markdown("**👁️ Как должна выглядеть готовая страница:**")
                st.markdown('<div class="preview-label">✨ Живой предпросмотр</div>', unsafe_allow_html=True)
                
                full_html = render_html_preview(code)
                st.components.v1.html(full_html, height=350, scrolling=True)

    # ---------- ВИКТОРИНА ----------
    elif st.session_state.game_type == "quiz" and st.session_state.quiz_questions:
        questions = st.session_state.quiz_questions
        total = len(questions)
        idx = st.session_state.current_question

        st.markdown("### 📝 ВИКТОРИНА")
        st.markdown(f"<span class='score-badge'>🏆 Счёт: {st.session_state.score} / {total}</span>", unsafe_allow_html=True)
        st.progress(idx / total if total > 0 else 0)
        st.markdown("---")

        if idx < total:
            q = questions[idx]
            st.markdown(f"**Вопрос {idx + 1} из {total}**")
            st.markdown(f"### {q['question']}")

            answer = st.radio("Выберите ответ:", q['options'], key=f"quiz_q_{idx}", disabled=st.session_state.answer_locked)

            if not st.session_state.answer_locked:
                if st.button("✅ Ответить", key=f"answer_{idx}"):
                    correct_idx = q['correct']
                    if answer == q['options'][correct_idx]:
                        st.session_state.score += 1
                        st.session_state.result_message = "🎉 Правильно! +1 балл."
                        st.session_state.result_type = "correct"
                    else:
                        st.session_state.result_message = f"❌ Неправильно. Правильный ответ: {q['options'][correct_idx]}\n\n📚 {q.get('explanation', '')}"
                        st.session_state.result_type = "wrong"
                    st.session_state.answer_locked = True
                    st.session_state.show_result = True
                    st.rerun()

            render_game_footer(total, "quiz")
        else:
            st.balloons()
            st.success(f"🎉 Викторина завершена! Счёт: {st.session_state.score}/{total}")
            if st.button("🔄 Новая игра", key="new_quiz_end"):
                reset_game()
                st.rerun()

    # ---------- ПРАВДА ИЛИ ЛОЖЬ ----------
    elif st.session_state.game_type == "truefalse" and st.session_state.quiz_questions:
        statements = st.session_state.quiz_questions
        total = len(statements)
        idx = st.session_state.current_question

        st.markdown("### ✅ ПРАВДА ИЛИ ЛОЖЬ?")
        st.markdown(f"<span class='score-badge'>🏆 Счёт: {st.session_state.score} / {total}</span>", unsafe_allow_html=True)
        st.progress(idx / total if total > 0 else 0)
        st.markdown("---")

        if idx < total:
            item = statements[idx]
            st.markdown(f"**Утверждение {idx + 1} из {total}**")
            st.markdown(f"### {item['statement']}")

            if not st.session_state.answer_locked:
                col_t1, col_t2 = st.columns(2)
                with col_t1:
                    if st.button("✅ Правда", key=f"true_{idx}"):
                        if item['is_true']:
                            st.session_state.score += 1
                            st.session_state.result_message = "🎉 Правильно! Это правда. +1 балл."
                            st.session_state.result_type = "correct"
                        else:
                            st.session_state.result_message = f"❌ Неправильно! Это ложь.\n\n📚 {item.get('explanation', '')}"
                            st.session_state.result_type = "wrong"
                        st.session_state.answer_locked = True
                        st.session_state.show_result = True
                        st.rerun()
                with col_t2:
                    if st.button("❌ Ложь", key=f"false_{idx}"):
                        if not item['is_true']:
                            st.session_state.score += 1
                            st.session_state.result_message = "🎉 Правильно! Это ложь. +1 балл."
                            st.session_state.result_type = "correct"
                        else:
                            st.session_state.result_message = f"❌ Неправильно! Это правда.\n\n📚 {item.get('explanation', '')}"
                            st.session_state.result_type = "wrong"
                        st.session_state.answer_locked = True
                        st.session_state.show_result = True
                        st.rerun()

            render_game_footer(total, "tf")
        else:
            st.balloons()
            st.success(f"🎉 Игра завершена! Счёт: {st.session_state.score}/{total}")
            if st.button("🔄 Новая игра", key="new_tf_end"):
                reset_game()
                st.rerun()

    # ---------- НАЙДИ ПАРУ ----------
    elif st.session_state.game_type == "match" and st.session_state.quiz_questions:
        pairs = st.session_state.quiz_questions
        total = len(pairs)
        matched = st.session_state.matched_pairs

        st.markdown("### 🃏 НАЙДИ ПАРУ")
        st.markdown(f"<span class='score-badge'>🏆 Найдено пар: {len(matched)} / {total}</span>", unsafe_allow_html=True)
        st.progress(len(matched) / total if total > 0 else 0)
        st.markdown("---")

        if len(matched) < total:
            remaining_terms = [p["term"] for i, p in enumerate(pairs) if i not in matched]
            matched_defs = {pairs[i]["definition"] for i in matched}
            remaining_defs = [d for d in st.session_state.shuffled_defs if d not in matched_defs]

            col_term, col_def = st.columns(2)
            with col_term:
                st.markdown("**🔤 Термины:**")
                selected_term = st.radio("Выберите термин:", remaining_terms, key="match_term")
            with col_def:
                st.markdown("**📖 Определения:**")
                selected_def = st.radio("Выберите определение:", remaining_defs, key="match_def")

            if st.button("✅ Проверить пару"):
                correct_def = next((p["definition"] for p in pairs if p["term"] == selected_term), None)
                if selected_def == correct_def:
                    pair_idx = next(i for i, p in enumerate(pairs) if p["term"] == selected_term)
                    st.session_state.matched_pairs = matched | {pair_idx}
                    st.session_state.match_score += 1
                    st.success(f"🎉 Правильно! «{selected_term}» → «{correct_def}»")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(f"❌ Неверно. Правильное определение: {correct_def}")
        else:
            st.balloons()
            st.success(f"🎉 Все пары найдены! Очков: {st.session_state.match_score}/{total}")
            if st.button("🔄 Новая игра", key="new_match_end"):
                reset_game()
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== ФУТЕР ====================
st.markdown("---")
st.markdown("""
<div class="footer">
<p style="font-size: 1.1rem;">✨ Универсальный генератор на базе AI через OpenRouter ✨</p>
<p style="font-size: 0.8rem; color: #888;">🔑 Бесплатный API ключ доступен на OpenRouter</p>
</div>
""", unsafe_allow_html=True)
