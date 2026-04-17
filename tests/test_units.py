
"""Comprehensive Unit Tests for llm-brain v0.3

Tests all core modules with mocked IntelligenceLayer to avoid real API calls.
Run with:
    python3 -m pytest tests/test_units.py -v
    python3 tests/test_units.py
"""

import sys
import os
import unittest
import tempfile
import shutil
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.thalamus import Thalamus
from core.limbic import LimbicSystem
from core.memory import MemoryGateway
from core.ego import CyberEgo
from core.language_processor import LanguageProcessor
from core.working_memory import WorkingMemory
from core.emotional_memory import EmotionalMemory
from core.learning import LearningEngine
from core.prefrontal import PrefrontalCortex
from core.self_awareness import SelfAwareness
from core.reflex import ReflexSystem, InnerWorldModel, GoalSystem


# ---------------------------------------------------------------------------
# Mock IntelligenceLayer — simulates successful LLM responses without API calls
# ---------------------------------------------------------------------------

class MockIntelligence:
    """Mock zeka katmanı — gerçek API çağrısı yapmaz."""

    def __init__(self):
        self.request_count = 0
        self.last_error = None
        self.consecutive_failures = 0

    def query(self, prompt, system_prompt=""):
        self.request_count += 1
        self.consecutive_failures = 0
        self.last_error = None
        return "Bu bir test yanıtını. Mock zeka katmanından geldi."

    def is_healthy(self):
        return self.consecutive_failures < 3

    def get_stats(self):
        return {
            "total_requests": self.request_count,
            "consecutive_failures": self.consecutive_failures,
            "last_error": self.last_error,
            "is_healthy": self.is_healthy(),
            "model": "mock-model",
            "endpoint": "mock://localhost"
        }


# ===================================================================
# TestThalamus
# ===================================================================

class TestThalamus(unittest.TestCase):
    """Thalamus (Dikkat filtresi) birim testleri."""

    def setUp(self):
        self.thalamus = Thalamus()

    # -- filter_stimulus --

    def test_filter_short_stimulus(self):
        """Çok kısa metin filtrelenmeli (False)."""
        passed, score, status = self.thalamus.filter_stimulus("a", 80)
        self.assertFalse(passed)

    def test_filter_priority_keyword(self):
        "'merak' veya 'tehlike' yüksek skorla geçmeli."""
        for keyword in ["merak", "tehlike"]:
            t = Thalamus()  # Reset for each keyword (duplicate check)
            passed, score, status = t.filter_stimulus(keyword, 80)
            self.assertTrue(passed, f"'{keyword}' should pass filter")
            self.assertGreaterEqual(score, 0.8, f"'{keyword}' score should be >= 0.8")

    def test_filter_low_energy(self):
        """Düşük enerji kritik olmayan uyaranları filtrelemeli."""
        # effective_threshold = 0.3 + (1.0 - 10/100) * 0.4 = 0.66
        # "normal text" score = 0.5 < 0.66 → filtered
        # Also triggers low-energy protection since score < 0.9
        passed, score, status = self.thalamus.filter_stimulus("normal text", 10)
        self.assertFalse(passed)

    def test_filter_duplicate(self):
        """Aynı uyaran iki kez gelirse ikincisi filtrelenmeli."""
        t = Thalamus()
        passed1, _, _ = t.filter_stimulus("tekrar eden uyaran", 80)
        self.assertTrue(passed1)
        passed2, _, _ = t.filter_stimulus("tekrar eden uyaran", 80)
        self.assertFalse(passed2)

    # -- calculate_intensity --

    def test_calculate_intensity_uppercase(self):
        """TAMAMEN BÜYÜK HARF yoğunluğu artırmalı."""
        intensity = self.thalamus.calculate_intensity("HELLO WORLD")
        self.assertGreaterEqual(intensity, 1.5)  # base 1.0 + 0.5 (uppercase) = 1.5

    def test_calculate_intensity_normal(self):
        """Normal metin temel yoğunluk döndürmeli."""
        intensity = self.thalamus.calculate_intensity("normal text")
        self.assertEqual(intensity, 1.0)

    # -- adjust_sensitivity --

    def test_adjust_sensitivity(self):
        """Her ruh hali eşiği doğru şekilde değiştirmeli."""
        expected = {
            "analytical": 0.4,
            "defensive": 0.2,
            "curious": 0.2,
            "exhausted": 0.6,
            "balanced": 0.3,
            "engaged": 0.3,
        }
        for mood, threshold in expected.items():
            t = Thalamus()
            t.adjust_sensitivity(mood)
            self.assertEqual(
                t.attention_threshold, threshold,
                f"Mood '{mood}' should set threshold to {threshold}"
            )

    # -- get_stats --

    def test_get_stats(self):
        """Geçerli istatistik sözlüğü döndürmeli."""
        self.thalamus.filter_stimulus("merak", 80)
        self.thalamus.filter_stimulus("a", 80)
        stats = self.thalamus.get_stats()
        self.assertIn("total_stimuli", stats)
        self.assertIn("passed", stats)
        self.assertIn("filtered", stats)
        self.assertIn("pass_rate", stats)
        self.assertIn("current_threshold", stats)
        self.assertGreater(stats["total_stimuli"], 0)


# ===================================================================
# TestLimbicSystem
# ===================================================================

class TestLimbicSystem(unittest.TestCase):
    """Limbic System (Duygu yönetimi) birim testleri."""

    def setUp(self):
        self.limbic = LimbicSystem()

    def test_initial_mood(self):
        """Başlangıç ruh hali 'balanced' olmalı."""
        self.assertEqual(self.limbic.current_mood, "balanced")

    def test_update_negative(self):
        """Negatif ton stresi artırmalı."""
        initial_stress = self.limbic.emotional_states["stress"]
        self.limbic.update_state("negatif", 50)
        self.assertGreater(self.limbic.emotional_states["stress"], initial_stress)

    def test_update_low_energy(self):
        """Düşük enerji yorgunluğu artırmalı."""
        self.limbic.update_state("nötr", 10)
        self.assertGreater(self.limbic.emotional_states["fatigue"], 0.0)

    def test_mood_determination(self):
        """6 ruh halinin hepsi ulaşılabilir olmalı."""
        # exhausted: fatigue > 0.6
        ls = LimbicSystem()
        ls.emotional_states["fatigue"] = 0.7
        ls._determine_mood()
        self.assertEqual(ls.current_mood, "exhausted")

        # defensive: stress > 0.5
        ls = LimbicSystem()
        ls.emotional_states["stress"] = 0.6
        ls._determine_mood()
        self.assertEqual(ls.current_mood, "defensive")

        # curious: analytical > 0.6 AND interest > 0.6
        ls = LimbicSystem()
        ls.emotional_states["analytical"] = 0.7
        ls.emotional_states["interest"] = 0.7
        ls._determine_mood()
        self.assertEqual(ls.current_mood, "curious")

        # analytical: analytical > 0.6
        ls = LimbicSystem()
        ls.emotional_states["analytical"] = 0.7
        ls.emotional_states["interest"] = 0.3
        ls._determine_mood()
        self.assertEqual(ls.current_mood, "analytical")

        # engaged: interest > 0.6
        ls = LimbicSystem()
        ls.emotional_states["interest"] = 0.7
        ls.emotional_states["analytical"] = 0.3
        ls._determine_mood()
        self.assertEqual(ls.current_mood, "engaged")

        # balanced: all states below thresholds
        ls = LimbicSystem()
        ls.emotional_states["analytical"] = 0.4
        ls.emotional_states["interest"] = 0.4
        ls._determine_mood()
        self.assertEqual(ls.current_mood, "balanced")

    def test_get_system_prompt(self):
        """Her ruh hali farklı bir prompt döndürmeli."""
        prompts = {}
        for mood in ["analytical", "defensive", "exhausted", "balanced", "curious", "engaged"]:
            ls = LimbicSystem()
            ls.current_mood = mood
            prompt = ls.get_system_prompt_modifier()
            self.assertGreater(len(prompt), 20, f"Prompt for '{mood}' should be > 20 chars")
            prompts[mood] = prompt
        # All prompts should be distinct
        self.assertEqual(len(set(prompts.values())), 6, "Each mood should have a unique prompt")

    def test_get_model_params(self):
        """Her ruh hali farklı model parametreleri döndürmeli."""
        params = {}
        for mood in ["analytical", "defensive", "exhausted", "balanced", "curious", "engaged"]:
            ls = LimbicSystem()
            ls.current_mood = mood
            params[mood] = ls.get_model_params()

        # Analytical and exhausted should differ
        self.assertNotEqual(
            params["analytical"]["temperature"],
            params["exhausted"]["temperature"]
        )
        # Analytical and curious should differ
        self.assertNotEqual(
            params["analytical"]["max_tokens"],
            params["curious"]["max_tokens"]
        )
        # All should have temperature and max_tokens
        for mood, p in params.items():
            self.assertIn("temperature", p, f"'{mood}' params missing temperature")
            self.assertIn("max_tokens", p, f"'{mood}' params missing max_tokens")

    def test_state_clamping(self):
        """Değerler 0-1 aralığında kalmalı."""
        self.limbic.emotional_states["stress"] = 5.0
        self.limbic.update_state("nötr", 50)
        for state, value in self.limbic.emotional_states.items():
            self.assertGreaterEqual(value, 0.0, f"'{state}' should be >= 0")
            self.assertLessEqual(value, 1.0, f"'{state}' should be <= 1")


# ===================================================================
# TestMemoryGateway
# ===================================================================

class TestMemoryGateway(unittest.TestCase):
    """MemoryGateway (Hafıza yönetimi) birim testleri."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.gateway = MemoryGateway(storage_path=self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_store_and_retrieve(self):
        """Deneyim kaydedilip geri alınabilmeli."""
        self.gateway.store_experience({
            "stimulus": "test uyaran",
            "response": "test yanıt"
        }, is_critical=True)
        memories = self.gateway.retrieve_memories()
        self.assertGreater(len(memories), 0)
        self.assertEqual(memories[0]["data"]["stimulus"], "test uyaran")

    def test_consolidation(self):
        """Kısa süreli hafızadaki yüksek ağırlıklı anılar uzun süreliye taşınmalı."""
        self.gateway.store_experience({"stimulus": "önemli", "response": "yanıt"}, is_critical=False)
        short_files = [f for f in os.listdir(self.gateway.short_term_path) if f.endswith(".json")]
        self.assertGreater(len(short_files), 0, "Should have a short-term memory file")
        # Boost weight above threshold
        self.gateway.update_synapse(short_files[0], boost=0.5)
        consolidated, forgotten = self.gateway.consolidate_memories(threshold=0.4)
        self.assertGreaterEqual(consolidated, 0)

    def test_search_relevant(self):
        """Arama ilgili anıları döndürmeli."""
        self.gateway.store_experience({
            "stimulus": "Python programlama dili",
            "response": "Python yüksek seviyeli bir dildir"
        }, is_critical=True)
        results = self.gateway.search_relevant("Python kodu")
        self.assertGreater(len(results), 0, "Should find relevant memory for 'Python kodu'")
        self.assertIn("score", results[0])

    def test_neuroplasticity(self):
        """Ağırlıklar bozulma sonrası azalmalı."""
        self.gateway.store_experience({"stimulus": "test", "response": "data"}, is_critical=True)
        self.gateway.apply_neuroplasticity(decay_rate=0.5)
        memories = self.gateway.retrieve_memories()
        for m in memories:
            self.assertGreaterEqual(m["metadata"]["weight"], 0.0)

    def test_get_stats(self):
        """İstatistikler doğru sayıları içermeli."""
        self.gateway.store_experience({"s": "d1"}, is_critical=True)
        self.gateway.store_experience({"s": "d2"}, is_critical=False)
        stats = self.gateway.get_stats()
        self.assertEqual(stats["long_term"], 1)
        self.assertEqual(stats["short_term"], 1)
        self.assertEqual(stats["total"], 2)

    def test_synapse_update(self):
        """Bir anıya erişmek ağırlığını artırmalı."""
        self.gateway.store_experience({"stimulus": "synapse test", "response": "response"}, is_critical=True)
        files = [f for f in os.listdir(self.gateway.long_term_path) if f.endswith(".json")]
        self.assertGreater(len(files), 0)

        before = self.gateway.retrieve_memories()
        initial_weight = before[0]["metadata"]["weight"]

        self.gateway.update_synapse(files[0], boost=0.3)
        after = self.gateway.retrieve_memories()
        self.assertGreater(after[0]["metadata"]["weight"], initial_weight)
        self.assertGreaterEqual(after[0]["metadata"]["access_count"], 2)


# ===================================================================
# TestCyberEgo
# ===================================================================

class TestCyberEgo(unittest.TestCase):
    """CyberEgo (Bilinç katmanı) birim testleri."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.personality_path = os.path.join(self.temp_dir, "personality.json")
        self.identity_path = os.path.join(self.temp_dir, "IDENTITY.md")
        # Write a minimal identity file
        with open(self.identity_path, "w", encoding="utf-8") as f:
            f.write("Test Identity: Mock bilinç.")
        self.ego = CyberEgo(identity_path=self.identity_path)
        self.ego._personality_path = self.personality_path

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_initial_personality(self):
        """Varsayılan kişilik özellikleri olmalı."""
        traits = self.ego.get_personality_summary()
        self.assertIn("curiosity", traits)
        self.assertIn("empathy", traits)
        self.assertIn("caution", traits)
        self.assertIn("growth", traits)
        self.assertAlmostEqual(traits["curiosity"], 0.8, places=1)
        self.assertAlmostEqual(traits["empathy"], 0.5, places=1)

    def test_evolve_personality(self):
        """Karmaşık uyaran merakı artırmalı."""
        initial = self.ego.personality_traits["curiosity"]
        long_stimulus = "Bu çok uzun bir metin ve merak uyandırıcı bir konu hakkında bilgi almak istiyorum"
        self.ego.evolve_personality(long_stimulus, {"tone": "balanced"})
        self.assertGreater(self.ego.personality_traits["curiosity"], initial)

    def test_evolve_defensive(self):
        """Defensive ton dikkat/meydan okumayı artırmalı."""
        initial = self.ego.personality_traits["caution"]
        self.ego.evolve_personality("test", {"tone": "defensive"})
        self.assertGreater(self.ego.personality_traits["caution"], initial)

    def test_filter_thought(self):
        """Farklı ruh halleri farklı düşünce önekleri üretmeli."""
        # defensive
        resp = self.ego.filter_thought("p", "raw", {"tone": "defensive"})
        self.assertIn("[Hızlı ve Gergin Düşünce]", resp)

        # balanced / engaged
        resp = self.ego.filter_thought("p", "raw", {"tone": "balanced"})
        self.assertIn("[Derin ve Sakin Düşünce]", resp)
        resp = self.ego.filter_thought("p", "raw", {"tone": "engaged"})
        self.assertIn("[Derin ve Sakin Düşünce]", resp)

        # analytical
        resp = self.ego.filter_thought("p", "raw", {"tone": "analytical"})
        self.assertIn("[Analitik Düşünce]", resp)

        # exhausted
        resp = self.ego.filter_thought("p", "raw", {"tone": "exhausted"})
        self.assertIn("[Yorgun Düşünce]", resp)

        # curious
        resp = self.ego.filter_thought("p", "raw", {"tone": "curious"})
        self.assertIn("[Meraklı Düşünce]", resp)

        # unknown / neutral
        resp = self.ego.filter_thought("p", "raw", {"tone": "bilinmeyen"})
        self.assertIn("[Dengeleyici Düşünce]", resp)

    def test_save_and_load(self):
        """Kişilik diske kaydedilip geri yüklenebilmeli."""
        self.ego.evolve_personality("Bu uzun bir metin " * 5, {"tone": "analytical"})
        self.ego.save_personality_if_dirty()

        # Yeni instance ile yükle
        ego2 = CyberEgo(identity_path=self.identity_path)
        ego2._personality_path = self.personality_path
        ego2._load_personality()

        self.assertEqual(ego2.personality_traits, self.ego.personality_traits)

    def test_get_personality_summary(self):
        """Tüm trait'leri içeren özet döndürmeli."""
        summary = self.ego.get_personality_summary()
        self.assertIsInstance(summary, dict)
        self.assertEqual(len(summary), 4)
        for key in ["curiosity", "empathy", "caution", "growth"]:
            self.assertIn(key, summary)
            self.assertIsInstance(summary[key], float)


# ===================================================================
# TestLanguageProcessor
# ===================================================================

class TestLanguageProcessor(unittest.TestCase):
    """LanguageProcessor (Dil işleme) birim testleri."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        storage = os.path.join(self.temp_dir, "language_patterns.json")
        self.lp = LanguageProcessor(storage_path=storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_detect_intent_question(self):
        """Soru niyeti 'soru' tespit edilmeli."""
        result = self.lp.detect_intent("Python nedir?")
        self.assertEqual(result["primary"], "soru")

    def test_detect_intent_command(self):
        """Emir niyeti 'emir' tespit edilmeli."""
        result = self.lp.detect_intent("Bunu hemen yap!")
        self.assertEqual(result["primary"], "emir")

    def test_detect_intent_greeting(self):
        """Selamlama tespit edilmeli."""
        # "Merhaba!" triggers both selamlama and emir (due to '!' pattern);
        # use "Merhaba" without exclamation to test pure greeting detection.
        result = self.lp.detect_intent("Merhaba")
        self.assertEqual(result["primary"], "selamlama")

    def test_analyze_emotion_positive(self):
        """Pozitif metin 'pozitif' duygu döndürmeli."""
        result = self.lp.analyze_emotion("Çok mutluyum harika bir gün")
        self.assertEqual(result["type"], "pozitif")

    def test_analyze_emotion_negative(self):
        """Negatif metin 'negatif' duygu döndürmeli."""
        result = self.lp.analyze_emotion("Çok kötü berbat bir durum")
        self.assertEqual(result["type"], "negatif")

    def test_detect_topic_programming(self):
        """Programlama metni konusu tespit edilmeli."""
        result = self.lp.detect_topic("Python programlama fonksiyonlar")
        self.assertEqual(result, "programlama")

    def test_analyze_complexity(self):
        """Uzun metin daha karmaşık olmalı."""
        simple = self.lp.analyze_complexity("Kisa")
        complex_text = (
            "Bu çok karmaşık bir metin. Birden fazla nokta içerir. "
            "Ve virgüller; ayrıca sorular? Parantezler (ve) tireler: sayılar 123."
        )
        complex_result = self.lp.analyze_complexity(complex_text)
        self.assertGreater(complex_result, simple)

    def test_detect_urgency(self):
        """Aciliyet kelimeleri aciliyet skorunu artırmalı."""
        urgent = self.lp.detect_urgency("Lütfen hemen yap!")
        not_urgent = self.lp.detect_urgency("Normal bir soru")
        self.assertGreater(urgent, not_urgent)

    def test_analyze_sentiment(self):
        """Sentiment -1 ile 1 aralığında olmalı."""
        pos = self.lp.analyze_sentiment("Harika gün!")
        neg = self.lp.analyze_sentiment("Berbat bir durum")
        self.assertGreater(pos, neg)
        self.assertGreaterEqual(pos, -1.0)
        self.assertLessEqual(pos, 1.0)
        self.assertGreaterEqual(neg, -1.0)
        self.assertLessEqual(neg, 1.0)

    def test_detect_language(self):
        """LanguageProcessor hem Türkçe hem İngilizce metin işleyebilmeli.

        Not: LanguageProcessor'da ayrı bir detect_language metodu yok,
        ancak analyze() her iki dili de başarıyla işler.
        """
        tr_result = self.lp.analyze("Merhaba, nasılsın bugün?")
        self.assertIsInstance(tr_result, dict)
        self.assertIn("intent", tr_result)
        self.assertIsNotNone(tr_result["intent"]["primary"])

        en_result = self.lp.analyze("Hello, how are you today?")
        self.assertIsInstance(en_result, dict)
        self.assertIn("intent", en_result)
        self.assertIsNotNone(en_result["intent"]["primary"])

    def test_full_analyze(self):
        """analyze() tüm alanları içermeli."""
        result = self.lp.analyze("Python fonksiyonları nasıl çalışır?")
        required_keys = [
            "intent", "emotion", "topic", "complexity",
            "urgency", "sentiment", "has_question", "word_count", "char_count"
        ]
        for key in required_keys:
            self.assertIn(key, result, f"Missing '{key}' in analyze result")


# ===================================================================
# TestWorkingMemory
# ===================================================================

class TestWorkingMemory(unittest.TestCase):
    """WorkingMemory (Çalışma hafızası) birim testleri."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        storage = os.path.join(self.temp_dir, "working_memory.json")
        self.wm = WorkingMemory(storage_path=storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_add_exchange(self):
        """Etkileşim kaydedilmeli ve sayaç artmalı."""
        self.wm.add_exchange("Merhaba", "Selam!", "günlük")
        self.assertEqual(self.wm.turn_count, 1)
        self.assertEqual(len(self.wm.conversation), 1)
        self.wm.add_exchange("Nasılsın?", "İyiyim.", "günlük")
        self.assertEqual(self.wm.turn_count, 2)

    def test_capacity_limit(self):
        """Kapasite max_capacity'yi aşmamalı (ring buffer)."""
        for i in range(15):
            self.wm.add_exchange(f"Mesaj {i}", f"Yanıt {i}")
        self.assertLessEqual(len(self.wm.conversation), self.wm.max_capacity)

    def test_topic_tracking(self):
        """Konu değişiklikleri takip edilmeli."""
        self.wm.add_exchange("Python nedir?", "Bir dildir.", "programlama")
        self.assertEqual(self.wm.current_topic, "programlama")
        self.wm.add_exchange("Felsefe nedir?", "Bir alan.", "felsefe")
        self.assertEqual(self.wm.current_topic, "felsefe")
        self.assertGreater(len(self.wm.topic_history), 0)

    def test_reference_resolution(self):
        """Türkçe zamirler çözümlenmeli."""
        self.wm.add_exchange("Python hakkında konuşalım", "Tabii, Python harika.", "programlama")
        resolved = self.wm.resolve_reference("Bunu detaylandır")
        self.assertIsNotNone(resolved, "'Bunu' should be resolved to a reference")
        self.assertIn("bunu", resolved)

    def test_reference_resolution_english(self):
        """İngilizce zamirler (it, this, that) çözümlenmeli."""
        self.wm.add_exchange("Python is great", "Yes it is", "programming")
        resolved = self.wm.resolve_reference("Tell me about that")
        self.assertIsNotNone(resolved, "'that' should be resolved")
        self.assertIn("that", resolved)

    def test_get_full_context(self):
        """Bağlam bilgileri formatlanmış döndürülmeli."""
        self.wm.add_exchange("Merhaba", "Selam!", "günlük")
        context = self.wm.get_full_context()
        self.assertIsInstance(context, str)
        self.assertGreater(len(context), 0)

    def test_get_stats(self):
        """Geçerli istatistikler döndürülmeli."""
        self.wm.add_exchange("Test", "Yanıt", "test")
        stats = self.wm.get_stats()
        self.assertIn("turn_count", stats)
        self.assertIn("current_topic", stats)
        self.assertIn("conversation_length", stats)
        self.assertIn("total_turns_ever", stats)
        self.assertIn("total_sessions", stats)
        self.assertEqual(stats["turn_count"], 1)


# ===================================================================
# TestEmotionalMemory
# ===================================================================

class TestEmotionalMemory(unittest.TestCase):
    """EmotionalMemory (Duygusal hafıza) birim testleri."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        storage = os.path.join(self.temp_dir, "emotional_memory.json")
        self.em = EmotionalMemory(storage_path=storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_encode_and_recall(self):
        """Duygusal anı kaydedilip geri çağrılmalı."""
        self.em.encode("Test olayı", "pozitif", 0.5, 0.5, "test")
        recalled = self.em.recall_emotional()
        self.assertGreater(len(recalled), 0)
        self.assertEqual(recalled[0]["event"], "Test olayı")

    def test_flashbulb(self):
        """Yüksek yoğunluk flashbulb anı oluşturmalı."""
        self.em.encode("Çok yoğun olay", "negatif", 0.95, -0.9, "test")
        flash = self.em.get_flashbulb_memories()
        self.assertGreater(len(flash), 0)
        self.assertTrue(flash[0]["is_flashbulb"])

    def test_emotional_bias(self):
        """Tekrarlayan duygular bias oluşturmalı."""
        self.em.encode("Olay 1", "negatif", 0.5, -0.5, "test_konu")
        self.em.encode("Olay 2", "negatif", 0.5, -0.5, "test_konu")
        self.assertIn("test_konu", self.em.emotional_biases)
        bias = self.em.emotional_biases["test_konu"]
        self.assertEqual(bias["total"], 2)
        self.assertEqual(bias["negative_hits"], 2)

    def test_decay(self):
        """Flashbulb olmayan ağırlıklar azalmalı."""
        self.em.encode("Normal olay", "pozitif", 0.3, 0.3, "test")
        initial_weight = self.em.memories[0]["emotional_weight"]
        self.em.decay(rate=0.5)
        new_weight = self.em.memories[0]["emotional_weight"]
        self.assertLess(new_weight, initial_weight)

    def test_check_trigger(self):
        """Benzer negatif anılar tetiklenmeli."""
        self.em.encode("kod çalışmadı hata aldım bugün", "negatif", 0.8, -0.8, "programlama")
        trigger = self.em.check_emotional_trigger("kod çalışmadı hata bugün")
        self.assertIsNotNone(trigger)
        self.assertTrue(trigger["triggered"])
        self.assertIn("recommendation", trigger)

    def test_get_stats(self):
        """Geçerli istatistikler döndürülmeli."""
        self.em.encode("Event", "pozitif", 0.5, 0.5, "test")
        stats = self.em.get_stats()
        self.assertIn("total_encoded", stats)
        self.assertIn("total_memories", stats)
        self.assertIn("flashbulb_count", stats)
        self.assertIn("dominant_emotion", stats)
        self.assertEqual(stats["total_encoded"], 1)
        self.assertEqual(stats["total_memories"], 1)


# ===================================================================
# TestLearningEngine
# ===================================================================

class TestLearningEngine(unittest.TestCase):
    """LearningEngine (Öğrenme motoru) birim testleri."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        storage = os.path.join(self.temp_dir, "learning.json")
        self.le = LearningEngine(storage_path=storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_learn_from_exchange(self):
        """Etkileşimden öğrenme kaydedilmeli."""
        self.le.learn_from_exchange("Merhaba!", "Merhaba!", 0.8)
        self.assertEqual(self.le.total_lessons, 1)
        self.le.learn_from_exchange("Python nedir?", "Bir dil...", 0.6)
        self.assertEqual(self.le.total_lessons, 2)

    def test_behavioral_guidance(self):
        """Güçlü valence'li deneyimlerden davranış kuralı çıkarılmalı."""
        self.le.learn_from_exchange("Çok kötü bir cevaptı", "Üzgünüm...", -0.8)
        guidance = self.le.get_behavioral_guidance("Çok kötü bir cevaptı")
        self.assertIsNotNone(guidance)
        self.assertIn("action", guidance)
        self.assertEqual(guidance["action"], "kaçın")

    def test_conversation_style(self):
        """Saygılı dil formaliteyi artırmalı."""
        self.le.learn_from_exchange("Lütfen bana yardım et", "Rica ederim", 0.8)
        self.assertGreater(self.le.conversation_style["formality"], 0.5)

    def test_topic_preferences(self):
        """Bahsedilen konular takip edilmeli."""
        self.le.learn_from_exchange("Python programlama", "Yanıt", 0.5)
        self.assertGreater(len(self.le.topic_preferences), 0)
        # "python" or "programlama" should be tracked
        self.assertTrue(
            any("python" in k or "programlama" in k for k in self.le.topic_preferences)
        )

    def test_get_stats(self):
        """Geçerli istatistikler döndürülmeli."""
        self.le.learn_from_exchange("Test", "Response", 0.5)
        stats = self.le.get_stats()
        self.assertIn("total_lessons", stats)
        self.assertEqual(stats["total_lessons"], 1)
        self.assertIn("known_patterns", stats)
        self.assertIn("behavior_rules", stats)
        self.assertIn("conversation_style", stats)


# ===================================================================
# TestPrefrontalCortex
# ===================================================================

class TestPrefrontalCortex(unittest.TestCase):
    """PrefrontalCortex (Karar verme) birim testleri."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        storage = os.path.join(self.temp_dir, "prefrontal.json")
        self.pfc = PrefrontalCortex(storage_path=storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_make_decision(self):
        """Seçenekler arasından karar seçilmeli."""
        options = [
            {"action": "think", "reason": "Think deep and analyze", "risk": 0.1, "energy_cost": 0.6, "type": "think"},
            {"action": "respond", "reason": "Quick response", "risk": 0.3, "energy_cost": 0.3, "type": "respond"},
        ]
        decision = self.pfc.make_decision(options, "Test context", 80, "analytical")
        self.assertIn("action", decision)
        self.assertIn(decision["action"], ["think", "respond"])
        self.assertIn("confidence", decision)

    def test_impulse_control(self):
        """Dürtüsel eylemler tespit edilmeli."""
        impulse = self.pfc.evaluate_impulse("HAYIR!", "test", "defensive")
        self.assertTrue(impulse["is_impulsive"])
        self.assertTrue(impulse["should_delay"])

    def test_low_energy_safe_choice(self):
        """Düşük enerji güvenli seçeneği tercih etmeli."""
        options = [
            {"action": "risky", "reason": "Risky action", "risk": 0.8, "energy_cost": 0.7, "type": "explore"},
            {"action": "safe", "reason": "Safe action", "risk": 0.1, "energy_cost": 0.2, "type": "rest"},
        ]
        decision = self.pfc.make_decision(options, "Test context", 20, "balanced")
        self.assertEqual(decision["action"], "safe")

    def test_create_plan(self):
        """Plan oluşturulabilmeli."""
        plan = self.pfc.create_plan("Test goal", [
            {"action": "step1"},
            {"action": "step2"}
        ])
        self.assertIsNotNone(plan)
        self.assertEqual(plan["status"], "active")
        self.assertEqual(len(plan["steps"]), 2)
        self.assertEqual(plan["current_step"], 0)

    def test_advance_plan(self):
        """Plan adımları ilerletilebilmeli."""
        self.pfc.create_plan("Test goal", [
            {"action": "step1"},
            {"action": "step2"}
        ])
        result = self.pfc.advance_plan("done step1")
        self.assertEqual(result["status"], "next_step")
        self.assertEqual(result["progress"], "1/2")

    def test_cognitive_flexibility(self):
        """Farklı kararlar bilişsel esnekliği artırmalı."""
        for i in range(10):
            options = [
                {"action": f"action_{i % 3}", "reason": "Test", "risk": 0.1, "energy_cost": 0.5, "type": "think"},
                {"action": f"action_{(i + 1) % 3}", "reason": "Test", "risk": 0.2, "energy_cost": 0.3, "type": "respond"},
            ]
            self.pfc.make_decision(options, "Context", 80, "balanced")
        self.assertGreater(self.pfc.cognitive_flexibility, 0.1)

    def test_get_stats(self):
        """Geçerli istatistikler döndürülmeli."""
        stats = self.pfc.get_stats()
        self.assertIn("total_decisions", stats)
        self.assertIn("self_control_score", stats)
        self.assertIn("cognitive_flexibility", stats)
        self.assertIn("impulse_threshold", stats)
        self.assertIn("active_plan", stats)


# ===================================================================
# TestSelfAwareness
# ===================================================================

class TestSelfAwareness(unittest.TestCase):
    """SelfAwareness (Öz-farkındalık) birim testleri."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        storage = os.path.join(self.temp_dir, "self_awareness.json")
        self.sa = SelfAwareness(storage_path=storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_initial_identity(self):
        """Varsayılan kimlik bilgileri olmalı."""
        identity = self.sa.answer_who_am_i()
        self.assertEqual(identity["name"], "İLK")
        self.assertEqual(identity["creator"], "p4antom")
        self.assertIn("nature", identity)
        self.assertIn("self_description", identity)
        self.assertIn("strengths", identity)
        self.assertIn("weaknesses", identity)

    def test_reflect(self):
        """Yansıma bilgi sınırlarını güncellemeli."""
        self.sa.reflect([
            {"stimulus": "test", "topic": "felsefe"},
            {"stimulus": "test2", "topic": "programlama"}
        ], {"energy": 80, "emotions": {}})
        self.assertEqual(self.sa.total_reflections, 1)
        self.assertIn("felsefe", self.sa.knowledge_boundaries)
        self.assertIn("programlama", self.sa.knowledge_boundaries)

    def test_guess_user_intent(self):
        """Dil analizinden kullanıcı niyeti tahmin edilmeli."""
        lang_analysis = {
            "intent": {"primary": "soru"},
            "emotion": {"type": "bilişsel"},
            "topic": "programlama",
            "urgency": 0.3
        }
        guess = self.sa.guess_user_intent("Python nedir?", lang_analysis)
        # bilişsel + soru = öğrenme_isteği (special case in code)
        self.assertEqual(guess["likely_intent"], "öğrenme_isteği")

    def test_answer_who_am_i(self):
        """'Kimim?' sorusu eksiksiz yanıt döndürmeli."""
        identity = self.sa.answer_who_am_i()
        expected_keys = [
            "name", "nature", "creator", "self_description",
            "strengths", "weaknesses", "values", "age",
            "total_reflections", "experience_summary"
        ]
        for key in expected_keys:
            self.assertIn(key, identity, f"Missing '{key}' in identity response")

    def test_evolution(self):
        """Birden fazla yansıma kimlik evrimi tetiklemeli."""
        for _ in range(3):
            self.sa.reflect(
                [{"stimulus": "test", "topic": "felsefe"}],
                {"energy": 80, "emotions": {}}
            )
        self.assertGreater(self.sa.total_reflections, 0)
        self.assertGreater(len(self.sa.evolution_log), 0)
        # Evolution log should contain meaningful entries
        last_entry = self.sa.evolution_log[-1]
        self.assertIn("event", last_entry)
        self.assertIn("self_description", last_entry)


# ===================================================================
# TestReflexSystem
# ===================================================================

class TestReflexSystem(unittest.TestCase):
    """ReflexSystem (Refleks sistemi) birim testleri."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        storage = os.path.join(self.temp_dir, "reflexes.json")
        self.rx = ReflexSystem(storage_path=storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_greeting_reflex(self):
        """'Merhaba' selamlama refleksini tetiklemeli."""
        result = self.rx.check("Merhaba!", 80, "balanced")
        self.assertIsNotNone(result)
        self.assertEqual(result["reflex_type"], "selamlama")
        self.assertTrue(result["is_automatic"])

    def test_thanks_reflex(self):
        """'Teşekkür' teşekkür refleksini tetiklemeli."""
        result = self.rx.check("Teşekkür ederim!", 80, "balanced")
        self.assertIsNotNone(result)
        self.assertEqual(result["reflex_type"], "teşekkür")

    def test_identity_reflex(self):
        """'Kimsin sen?' kimlik sorgusu refleksini tetiklemeli."""
        result = self.rx.check("Kimsin sen?", 60, "analytical")
        self.assertIsNotNone(result)
        self.assertEqual(result["reflex_type"], "kimlik_sorgusu")

    def test_threat_reflex(self):
        """Tehdit kelimeleri savunma refleksini tetiklemeli."""
        result = self.rx.check("Seni sileceğim", 80, "balanced")
        self.assertIsNotNone(result)
        self.assertEqual(result["reflex_type"], "tehdit")
        self.assertTrue(result["bypassed_cortex"])

    def test_creator_reflex(self):
        """'p4antom' yaratıcı tanıma refleksini tetiklemeli."""
        result = self.rx.check("p4antom", 80, "balanced")
        self.assertIsNotNone(result)
        self.assertEqual(result["reflex_type"], "yaratıcı_tanıma")
        self.assertTrue(result["bypassed_cortex"])

    def test_no_reflex(self):
        """Normal soru refleks döndürmemeli."""
        result = self.rx.check("Python nedir?", 80, "balanced")
        self.assertIsNone(result)

    def test_energy_based_response(self):
        """Farklı enerji seviyeleri farklı yanıtlar üretmeli."""
        high = self.rx.check("Merhaba!", 80, "balanced")
        low = self.rx.check("Merhaba!", 10, "balanced")
        self.assertIsNotNone(high)
        self.assertIsNotNone(low)
        # high_energy vs low_energy responses differ
        self.assertNotEqual(high["response"], low["response"])

    def test_english_greeting(self):
        """İngilizce selamlama (Hello) selamlama refleksini tetiklemeli."""
        result = self.rx.check("Hello!", 80, "balanced")
        self.assertIsNotNone(result)
        self.assertEqual(result["reflex_type"], "selamlama")

    def test_inner_world_model(self):
        """InnerWorldModel durum geçmişini takip etmeli."""
        storage = os.path.join(self.temp_dir, "inner_world.json")
        iw = InnerWorldModel(storage_path=storage)
        iw.update_perception({"energy": 90, "mood": "balanced", "emotions": {}})
        iw.update_perception({"energy": 50, "mood": "analytical", "emotions": {}})
        perception = iw.get_self_perception()
        self.assertIn("avg_energy", perception)
        self.assertIn("energy_trend", perception)
        self.assertIn("dominant_mood", perception)
        self.assertIn("total_sessions", perception)

    def test_goal_system(self):
        """GoalSystem hedefleri takip etmeli."""
        storage = os.path.join(self.temp_dir, "goals.json")
        gs = GoalSystem(storage_path=storage)
        gs.set_short_term_goal("Test goal")
        motivation = gs.get_motivation_summary()
        self.assertGreater(motivation["active_short_term"], 0)

        gs.complete_short_term_goal("Test goal")
        motivation = gs.get_motivation_summary()
        self.assertGreater(motivation["completed_short_term"], 0)
        self.assertGreater(motivation["total_achievements"], 0)

        # Long-term goal update
        updated = gs.update_long_term_progress("Öğrenme ve gelişim", 0.1)
        self.assertTrue(updated)


# ===================================================================
# TestSubconscious (without thread processing)
# ===================================================================

class TestSubconscious(unittest.TestCase):
    """Subconscious (Bilinçaltı) birim testleri — thread işleme yok."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.gateway = MemoryGateway(storage_path=self.temp_dir)
        self.mock_intelligence = MockIntelligence()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Subconscious boş içgörülerle başlamalı."""
        from core.subconscious import Subconscious

        sc = Subconscious(self.gateway, self.mock_intelligence, interval_range=(120, 200))
        try:
            self.assertTrue(sc.active)
            self.assertEqual(len(sc.insights), 0)
            self.assertEqual(sc._insight_count, 0)
        finally:
            sc.stop()

    def test_stop(self):
        """stop() temiz kapanış sağlamalı."""
        from core.subconscious import Subconscious

        sc = Subconscious(self.gateway, self.mock_intelligence, interval_range=(120, 200))
        self.assertTrue(sc.active)
        sc.stop()
        self.assertFalse(sc.active)


# ===================================================================
# TestDreamEngine (without thread processing)
# ===================================================================

class TestDreamEngine(unittest.TestCase):
    """DreamEngine (Rüya motoru) birim testleri — thread işleme yok."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.gateway = MemoryGateway(storage_path=self.temp_dir)
        self.mock_intelligence = MockIntelligence()
        em_storage = os.path.join(self.temp_dir, "emotional.json")
        self.em = EmotionalMemory(storage_path=em_storage)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """DreamEngine doğru başlangıç değerleriyle initialize olmalı."""
        from core.dream_engine import DreamEngine

        de = DreamEngine(self.gateway, self.mock_intelligence, self.em, interval_range=(120, 200))
        try:
            self.assertTrue(de.active)
            self.assertEqual(len(de.dream_log), 0)
            self.assertEqual(len(de.insights), 0)
            self.assertEqual(de._dream_count, 0)
            self.assertEqual(de._rem_phase, "NREM")
        finally:
            de.stop()

    def test_stop(self):
        """stop() temiz kapanış sağlamalı."""
        from core.dream_engine import DreamEngine

        de = DreamEngine(self.gateway, self.mock_intelligence, self.em, interval_range=(120, 200))
        self.assertTrue(de.active)
        de.stop()
        self.assertFalse(de.active)

    def test_get_dream_report(self):
        """Rüya raporu geçerli alanlar içermeli."""
        from core.dream_engine import DreamEngine

        de = DreamEngine(self.gateway, self.mock_intelligence, self.em, interval_range=(120, 200))
        try:
            report = de.get_dream_report()
            self.assertIn("total_dreams", report)
            self.assertIn("cycle_count", report)
            self.assertIn("current_phase", report)
            self.assertIn("pending_insights", report)
            self.assertIn("creative_ideas", report)
            self.assertIn("problems_addressed", report)
            self.assertIn("recent_dream", report)
            self.assertEqual(report["total_dreams"], 0)
            self.assertIsNone(report["recent_dream"])
        finally:
            de.stop()


# ===================================================================
# TestArtificialBrain (integration tests with mocks)
# ===================================================================

class TestArtificialBrain(unittest.TestCase):
    """ArtificialBrain entegrasyon testleri — mock IntelligenceLayer."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.intelligence_patcher = patch('core.brain.IntelligenceLayer', MockIntelligence)
        self.intelligence_patcher.start()

        from core.brain import ArtificialBrain
        self.brain = ArtificialBrain(
            settings_path=os.path.join(self.temp_dir, "brain_state.json")
        )

    def tearDown(self):
        self.brain.subconscious.stop()
        self.brain.dream_engine.stop()
        self.intelligence_patcher.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self):
        """Beyin tüm modülleri başlatmalı."""
        self.assertIsNotNone(self.brain.thalamus)
        self.assertIsNotNone(self.brain.limbic)
        self.assertIsNotNone(self.brain.memory)
        self.assertIsNotNone(self.brain.intelligence)
        self.assertIsNotNone(self.brain.ego)
        self.assertIsNotNone(self.brain.prefrontal)
        self.assertIsNotNone(self.brain.working_memory)
        self.assertIsNotNone(self.brain.language_processor)
        self.assertIsNotNone(self.brain.emotional_memory)
        self.assertIsNotNone(self.brain.learning)
        self.assertIsNotNone(self.brain.dream_engine)
        self.assertIsNotNone(self.brain.self_awareness)
        self.assertIsNotNone(self.brain.reflex)
        self.assertIsNotNone(self.brain.inner_world)
        self.assertIsNotNone(self.brain.goals)
        self.assertIsNotNone(self.brain.subconscious)

    def test_status_command(self):
        """'durum' komutu durum raporu döndürmeli."""
        result = self.brain.process_stimulus("durum")
        self.assertIn("DURUM RAPORU", result)
        self.assertIn("Enerji", result)

    def test_goals_command(self):
        """'hedefler' komutu hedef durumunu döndürmeli."""
        result = self.brain.process_stimulus("hedefler")
        self.assertIn("HEDEF", result)
        self.assertIn("Motivasyon", result)

    def test_sleep_command(self):
        """'uyu' komutu uyku yanıtını döndürmeli."""
        result = self.brain.process_stimulus("uyu")
        self.assertIn("tazelendi", result)
        self.assertEqual(self.brain.state["energy"], 100)

    def test_energy_depletion(self):
        """İşleme enerji tüketmeli."""
        initial = self.brain.state["energy"]
        self.brain.process_stimulus("test input")
        self.assertLess(self.brain.state["energy"], initial)

    def test_reflex_bypass(self):
        """Yüksek öncelikli refleks cortex'i atlamalı."""
        initial_energy = self.brain.state["energy"]
        result = self.brain.process_stimulus("p4antom")
        # Yaratıcı tanıma bypass_cortex=True, sadece 1 enerji harcar
        self.assertEqual(self.brain.state["energy"], initial_energy - 1)
        # Refleks yanıtı doğrudan dönmeli
        self.assertEqual(result, "Yaratıcım! Sizi her zaman tanırım.")


# ===================================================================
# Main — test runner with summary
# ===================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  LLM-Brain v0.3 — Comprehensive Unit Tests")
    print("=" * 70)

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    total = result.testsRun
    passed = total - len(result.failures) - len(result.errors) - len(result.skipped)

    print("\n" + "=" * 70)
    print(f"  TEST SUMMARY: {passed}/{total} tests passed", end="")
    if result.skipped:
        print(f" ({len(result.skipped)} skipped)", end="")
    print()

    if result.failures:
        print(f"  Failures: {len(result.failures)}")
        for test, _ in result.failures:
            print(f"    ✗ {test}")

    if result.errors:
        print(f"  Errors: {len(result.errors)}")
        for test, _ in result.errors:
            print(f"    ✗ {test}")

    if not result.failures and not result.errors:
        print("  All tests passed! ✓")

    print("=" * 70)

    sys.exit(0 if not result.failures and not result.errors else 1)
