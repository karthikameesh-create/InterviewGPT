import streamlit as st

from utils.gemini_analyzer import generate_aptitude_questions

import time
# ===================================
# AI APTITUDE ENGINE
# ===================================

class AptitudeEngine:


    # ===================================
    # START TEST
    # ===================================

    @staticmethod
    def start_test(

        company,

        role,

        test_type,

        difficulty,

        num_questions

    ):

        questions = generate_aptitude_questions(

            company=company,

            role=role,

            test_type=test_type,

            difficulty=difficulty,

            num_questions=num_questions

        )

        # -----------------------------
        # Store Test Configuration
        # -----------------------------

        st.session_state["last_aptitude_company"] = company

        st.session_state["last_aptitude_role"] = role

        st.session_state["last_aptitude_test_type"] = test_type

        st.session_state["last_aptitude_difficulty"] = difficulty

        st.session_state["last_aptitude_questions_count"] = num_questions

        # -----------------------------
        # Store Questions
        # -----------------------------

        st.session_state["aptitude_questions"] = questions

        # -----------------------------
        # Reset Progress
        # -----------------------------

        st.session_state["current_aptitude_question"] = 0

        st.session_state["aptitude_answers"] = {}

        st.session_state["aptitude_score"] = 0

        st.session_state["aptitude_started"] = True

        st.session_state["aptitude_completed"] = False

        st.session_state["aptitude_report"] = ""

        st.session_state["aptitude_learning_plan"] = ""

        st.session_state["aptitude_statistics"] = {}

        st.session_state["aptitude_start_time"] = None

        st.session_state["question_start_time"] = None


    # ===================================
    # RESET TEST
    # ===================================

    @staticmethod
    def reset_test():

        st.session_state["aptitude_questions"] = []

        st.session_state["current_aptitude_question"] = 0

        st.session_state["aptitude_answers"] = {}

        st.session_state["aptitude_score"] = 0

        st.session_state["aptitude_started"] = False

        st.session_state["aptitude_completed"] = False

        st.session_state["aptitude_report"] = ""

        st.session_state["aptitude_learning_plan"] = ""

        st.session_state["aptitude_statistics"] = {}

        st.session_state["aptitude_start_time"] = None

        st.session_state["question_start_time"] = None


    # ===================================
    # GENERATE NEW TEST
    # ===================================

    @staticmethod
    def generate_new_test():

        AptitudeEngine.start_test(

            company=st.session_state.get(
                "last_aptitude_company",
                ""
            ),

            role=st.session_state.get(
                "last_aptitude_role",
                ""
            ),

            test_type=st.session_state.get(
                "last_aptitude_test_type",
                "Mixed"
            ),

            difficulty=st.session_state.get(
                "last_aptitude_difficulty",
                "Medium"
            ),

            num_questions=st.session_state.get(
                "last_aptitude_questions_count",
                20
            )

        )
    # ===================================
    # GET CURRENT QUESTION
    # ===================================

    @staticmethod
    def get_current_question():

        questions = st.session_state.get(
            "aptitude_questions",
            []
        )

        if len(questions) == 0:
            return None

        current = st.session_state.get(
            "current_aptitude_question",
            0
        )

        return questions[current]


    # ===================================
    # GET CURRENT QUESTION NUMBER
    # ===================================

    @staticmethod
    def get_current_question_number():

        return (
            st.session_state.get(
                "current_aptitude_question",
                0
            ) + 1
        )


    # ===================================
    # SAVE ANSWER
    # ===================================

    @staticmethod
    def save_answer(

        question_number,

        selected_option,

        time_taken=0,

        marked_for_review=False

    ):

        answers = st.session_state.get(
            "aptitude_answers",
            {}
        )

        answers[question_number] = {

            "selected": selected_option,

            "time_taken": time_taken,

            "marked_for_review": marked_for_review

        }

        st.session_state[
            "aptitude_answers"
        ] = answers


    # ===================================
    # GET SAVED ANSWER
    # ===================================

    @staticmethod
    def get_saved_answer(

        question_number

    ):

        answers = st.session_state.get(
            "aptitude_answers",
            {}
        )

        if question_number not in answers:

            return None

        return answers[
            question_number
        ]["selected"]


    # ===================================
    # MARK / UNMARK REVIEW
    # ===================================

    @staticmethod
    def toggle_review(

        question_number

    ):

        answers = st.session_state.get(
            "aptitude_answers",
            {}
        )

        if question_number not in answers:

            answers[question_number] = {

                "selected": None,

                "time_taken": 0,

                "marked_for_review": True

            }

        else:

            answers[
                question_number
            ][
                "marked_for_review"
            ] = not answers[
                question_number
            ][
                "marked_for_review"
            ]

        st.session_state[
            "aptitude_answers"
        ] = answers


    # ===================================
    # NEXT QUESTION
    # ===================================

    @staticmethod
    def next_question():

        current = st.session_state.get(
            "current_aptitude_question",
            0
        )

        total = len(

            st.session_state.get(
                "aptitude_questions",
                []
            )

        )

        if current < total - 1:

            st.session_state[
                "current_aptitude_question"
            ] = current + 1


    # ===================================
    # PREVIOUS QUESTION
    # ===================================

    @staticmethod
    def previous_question():

        current = st.session_state.get(
            "current_aptitude_question",
            0
        )

        if current > 0:

            st.session_state[
                "current_aptitude_question"
            ] = current - 1


    # ===================================
    # GO TO QUESTION
    # ===================================

    @staticmethod
    def goto_question(

        question_number

    ):

        total = len(

            st.session_state.get(
                "aptitude_questions",
                []
            )

        )

        if 1 <= question_number <= total:

            st.session_state[
                "current_aptitude_question"
            ] = question_number - 1


    # ===================================
    # GET PROGRESS
    # ===================================

    @staticmethod
    def get_progress():

        total = len(

            st.session_state.get(
                "aptitude_questions",
                []
            )

        )

        current = st.session_state.get(
            "current_aptitude_question",
            0
        )

        answers = st.session_state.get(
            "aptitude_answers",
            {}
        )

        answered = 0

        marked = 0

        skipped = 0

        for value in answers.values():

            if value["selected"] is not None:

                answered += 1

            else:

                skipped += 1

            if value["marked_for_review"]:

                marked += 1

        progress = 0

        if total > 0:

            progress = (

                (current + 1)

                / total

            ) * 100

        return {

            "current": current + 1,

            "total": total,

            "answered": answered,

            "marked": marked,

            "skipped": skipped,

            "remaining": total - answered,

            "progress": progress

        } 



    # ===================================
    # START TIMER
    # ===================================

    @staticmethod
    def start_timer():

        if st.session_state.get(
            "aptitude_start_time"
        ) is None:

            st.session_state[
                "aptitude_start_time"
            ] = time.time()


    # ===================================
    # REMAINING TIME
    # ===================================

    @staticmethod
    def get_remaining_time(

        total_minutes

    ):

        if total_minutes == 0:

            return None

        AptitudeEngine.start_timer()

        elapsed = (

            time.time()

            -

            st.session_state[
                "aptitude_start_time"
            ]

        )

        remaining = (

            total_minutes * 60

        ) - elapsed

        if remaining < 0:

            remaining = 0

        minutes = int(

            remaining // 60

        )

        seconds = int(

            remaining % 60

        )

        return (

            minutes,

            seconds,

            remaining

        )


    # ===================================
    # CALCULATE SCORE
    # ===================================

    @staticmethod
    def calculate_score(

        negative_marking=False

    ):

        questions = st.session_state.get(

            "aptitude_questions",

            []

        )

        answers = st.session_state.get(

            "aptitude_answers",

            {}

        )

        score = 0

        correct = 0

        wrong = 0

        skipped = 0

        topic_stats = {}

        category_stats = {}

        for q in questions:

            qno = q["question_number"]

            topic = q["topic"]

            category = q["category"]

            correct_answer = q["correct_answer"]

            if topic not in topic_stats:

                topic_stats[topic] = {

                    "correct":0,

                    "wrong":0

                }

            if category not in category_stats:

                category_stats[category] = {

                    "correct":0,

                    "wrong":0

                }

            if qno not in answers:

                skipped += 1

                continue

            selected = answers[qno]["selected"]

            if selected == correct_answer:

                score += 1

                correct += 1

                topic_stats[topic]["correct"] += 1

                category_stats[category]["correct"] += 1

            else:

                wrong += 1

                topic_stats[topic]["wrong"] += 1

                category_stats[category]["wrong"] += 1

                if negative_marking:

                    score -= 0.25

        total = len(questions)

        accuracy = 0

        if total > 0:

            accuracy = (

                correct

                /

                total

            ) * 100

        st.session_state[

            "aptitude_score"

        ] = score

        st.session_state[

            "aptitude_statistics"

        ] = {

            "score": score,

            "correct": correct,

            "wrong": wrong,

            "skipped": skipped,

            "accuracy": accuracy,

            "total": total,

            "topic_stats": topic_stats,

            "category_stats": category_stats

        }

        return st.session_state[

            "aptitude_statistics"

        ]


    # ===================================
    # SUBMIT TEST
    # ===================================

    @staticmethod
    def submit_test(

        negative_marking=False

    ):

        stats = AptitudeEngine.calculate_score(

            negative_marking

        )

        st.session_state[

            "aptitude_completed"

        ] = True

        return stats


    # ===================================
    # GET STATISTICS
    # ===================================

    @staticmethod
    def get_statistics():

        return st.session_state.get(

            "aptitude_statistics",

            {}

        )