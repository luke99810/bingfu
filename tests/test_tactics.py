"""
Tactics Engine Tests (战术引擎测试)
Tests for Sun Tzu's Art of War tactics engine.
"""

import pytest
from bingfu.tactics import (
    TacticsEngine,
    SunTzuAgent,
    TacticType,
    TacticalContext
)


class TestTacticType:
    """Test TacticType enum"""

    def test_tactic_types_exist(self):
        """Test all tactic types are defined"""
        assert TacticType.AMBUSH.value == "伏击"
        assert TacticType.FEIGN_RETREAT.value == "佯退"
        assert TacticType.SURROUND.value == "包围"
        assert TacticType.HARASS.value == "骚扰"
        assert TacticType.STARVE.value == "断粮"
        assert TacticType.DECEIVE.value == "诈术"
        assert TacticType.SWIFT_STRIKE.value == "突袭"
        assert TacticType.DEFENSIVE.value == "防守"
        assert TacticType.FULL_ASSAULT.value == "全线进攻"
        assert TacticType.EXHAUSTION.value == "疲敌"
        assert TacticType.WAITING.value == "以逸待劳"
        assert TacticType.COUNTER.value == "反击"
        assert TacticType.PROBING.value == "试探"

    def test_tactic_type_count(self):
        """Test there are 13 tactics (one for each chapter)"""
        assert len(TacticType) == 13


class TestTacticalContext:
    """Test TacticalContext model"""

    def test_create_context(self):
        """Test creating a tactical context"""
        context = TacticalContext(
            self_strength=30000,
            enemy_strength=80000,
            terrain="山地",
            morale=80
        )
        assert context.self_strength == 30000
        assert context.enemy_strength == 80000
        assert context.terrain == "山地"
        assert context.morale == 80

    def test_default_morale(self):
        """Test default morale value"""
        context = TacticalContext(
            self_strength=30000,
            enemy_strength=80000
        )
        assert context.morale == 50

    def test_strength_ratio(self):
        """Test strength ratio calculation"""
        context = TacticalContext(
            self_strength=30000,
            enemy_strength=60000
        )
        ratio = context.self_strength / context.enemy_strength
        assert ratio == 0.5


class TestTacticsEngine:
    """Test TacticsEngine class"""

    def test_engine_creation(self):
        """Test creating a tactics engine"""
        engine = TacticsEngine()
        assert engine is not None

    def test_analyze_weak_vs_strong(self):
        """Test analysis when weak vs strong"""
        engine = TacticsEngine()
        context = TacticalContext(
            self_strength=30000,
            enemy_strength=80000,
            terrain="山地",
            morale=70
        )
        result = engine.analyze(context)

        assert "recommended_tactic" in result
        assert "recommended_strategy" in result
        assert "tactics" in result
        assert isinstance(result["tactics"], list)

    def test_analyze_strong_vs_weak(self):
        """Test analysis when strong vs weak"""
        engine = TacticsEngine()
        context = TacticalContext(
            self_strength=80000,
            enemy_strength=30000,
            terrain="平原",
            morale=90
        )
        result = engine.analyze(context)

        assert "recommended_tactic" in result
        assert len(result["tactics"]) > 0

    def test_analyze_balanced(self):
        """Test analysis when forces are balanced"""
        engine = TacticsEngine()
        context = TacticalContext(
            self_strength=50000,
            enemy_strength=50000,
            terrain="河流",
            morale=60
        )
        result = engine.analyze(context)

        assert "recommended_tactic" in result

    def test_analyze_low_morale(self):
        """Test analysis with low morale"""
        engine = TacticsEngine()
        context = TacticalContext(
            self_strength=50000,
            enemy_strength=40000,
            terrain="平原",
            morale=20
        )
        result = engine.analyze(context)

        assert "recommended_tactic" in result

    def test_analyze_high_morale(self):
        """Test analysis with high morale"""
        engine = TacticsEngine()
        context = TacticalContext(
            self_strength=30000,
            enemy_strength=60000,
            terrain="山地",
            morale=95
        )
        result = engine.analyze(context)

        assert "recommended_tactic" in result

    def test_get_tactics_for_situation(self):
        """Test getting tactics for specific situation"""
        engine = TacticsEngine()

        tactics = engine.get_tactics_for_situation(
            strength_ratio=0.5,
            morale=70,
            terrain="山地"
        )

        assert isinstance(tactics, list)
        assert len(tactics) > 0

    def test_get_tactics_for_overwhelming(self):
        """Test getting tactics for overwhelming force"""
        engine = TacticsEngine()

        tactics = engine.get_tactics_for_situation(
            strength_ratio=2.0,
            morale=90,
            terrain="平原"
        )

        assert isinstance(tactics, list)

    def test_get_chapter_quote(self):
        """Test getting chapter quotes"""
        engine = TacticsEngine()

        quote = engine.get_chapter_quote()
        assert isinstance(quote, str)
        assert len(quote) > 0

        quote_specific = engine.get_chapter_quote(TacticType.AMBUSH)
        assert isinstance(quote_specific, str)


class TestSunTzuAgent:
    """Test SunTzuAgent class"""

    def test_create_suntzu_agent(self):
        """Test creating a Sun Tzu agent"""
        agent = SunTzuAgent(name="孙子", role="军师")

        assert agent.name == "孙子"
        assert agent.role == "军师"
        assert agent.description is not None
        assert len(agent.description) > 0

    def test_analyze_battlefield(self):
        """Test battle analysis"""
        agent = SunTzuAgent(name="孙子")

        context = TacticalContext(
            self_strength=30000,
            enemy_strength=80000,
            terrain="山地",
            morale=70
        )
        result = agent.analyze_battlefield(context)

        assert isinstance(result, dict)
        assert "recommended_tactic" in result

    def test_provide_tactical_advice(self):
        """Test providing tactical advice"""
        agent = SunTzuAgent(name="孙子")

        advice = agent.provide_tactical_advice(
            self_strength=50000,
            enemy_strength=30000,
            terrain="平原"
        )

        assert isinstance(advice, str)
        assert len(advice) > 0

    def test_quote_chapter(self):
        """Test quoting specific chapter"""
        agent = SunTzuAgent(name="孙子")

        quote = agent.quote_chapter(TacticType.AMBUSH)
        assert isinstance(quote, str)
        assert "伏击" in quote or "战" in quote


class TestIntegration:
    """Integration tests"""

    def test_full_battle_analysis_flow(self):
        """Test complete battle analysis workflow"""
        # Create engine
        engine = TacticsEngine()

        # Create context
        context = TacticalContext(
            self_strength=30000,
            enemy_strength=80000,
            terrain="山地",
            morale=70
        )

        # Analyze
        result = engine.analyze(context)

        # Verify result
        assert result["recommended_tactic"] is not None
        assert len(result["tactics"]) > 0

        # Create Sun Tzu agent
        sunbin = SunTzuAgent(name="孙子", role="军师")

        # Get advice from Sun Tzu
        advice = sunbin.analyze_battle(
            self_strength=30000,
            enemy_strength=80000,
            terrain="山地",
            morale=70
        )

        assert isinstance(advice, str)
        assert len(advice) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
