"""
Unit tests for Memory module.
测试记忆模块
"""

import pytest
import tempfile
import os
import json
from bingfu.memory import Memory


class TestMemoryDict:
    """Test suite for in-memory (dict) Memory."""

    def test_create_dict_memory(self):
        """Test creating an in-memory memory."""
        memory = Memory(name="test_memory", memory_type="dict")
        assert memory.name == "test_memory"
        assert memory.memory_type == "dict"
        assert len(memory) == 0

    def test_store_and_retrieve(self):
        """Test storing and retrieving values."""
        memory = Memory(memory_type="dict")
        memory.store("name", "Zhang San")
        memory.store("age", 25)

        assert memory.retrieve("name") == "Zhang San"
        assert memory.retrieve("age") == 25

    def test_retrieve_default(self):
        """Test retrieving with default value."""
        memory = Memory(memory_type="dict")
        result = memory.retrieve("nonexistent", default="default_value")
        assert result == "default_value"

    def test_delete_existing_key(self):
        """Test deleting an existing key."""
        memory = Memory(memory_type="dict")
        memory.store("key1", "value1")
        memory.store("key2", "value2")

        result = memory.delete("key1")
        assert result is True
        assert memory.retrieve("key1") is None
        assert memory.retrieve("key2") == "value2"

    def test_delete_nonexistent_key(self):
        """Test deleting a nonexistent key."""
        memory = Memory(memory_type="dict")
        result = memory.delete("nonexistent")
        assert result is False

    def test_clear_memory(self):
        """Test clearing all memory."""
        memory = Memory(memory_type="dict")
        memory.store("key1", "value1")
        memory.store("key2", "value2")

        memory.clear()
        assert len(memory) == 0

    def test_all_data(self):
        """Test getting all data."""
        memory = Memory(memory_type="dict")
        memory.store("key1", "value1")
        memory.store("key2", "value2")

        all_data = memory.all()
        assert all_data == {"key1": "value1", "key2": "value2"}

    def test_all_returns_copy(self):
        """Test that all() returns a copy, not reference."""
        memory = Memory(memory_type="dict")
        memory.store("key1", "value1")

        all_data = memory.all()
        all_data["key1"] = "modified"
        assert memory.retrieve("key1") == "value1"

    def test_len(self):
        """Test memory length."""
        memory = Memory(memory_type="dict")
        assert len(memory) == 0

        memory.store("key1", "value1")
        assert len(memory) == 1

        memory.store("key2", "value2")
        assert len(memory) == 2

    def test_str_representation(self):
        """Test Memory string representation."""
        memory = Memory(name="TestMem", memory_type="dict")
        s = str(memory)
        assert "TestMem" in s
        assert "dict" in s
        assert "entries=0" in s

        memory.store("key", "value")
        s = str(memory)
        assert "entries=1" in s

    def test_complex_values(self):
        """Test storing complex values."""
        memory = Memory(memory_type="dict")

        complex_data = {
            "list": [1, 2, 3],
            "nested": {"a": 1, "b": 2},
            "tuple": (1, 2)
        }
        memory.store("complex", complex_data)
        result = memory.retrieve("complex")
        assert result == complex_data


class TestMemoryFile:
    """Test suite for file-based Memory."""

    def test_create_file_memory(self):
        """Test creating a file-based memory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test_memory.json")
            memory = Memory(
                name="file_memory",
                memory_type="file",
                file_path=file_path
            )
            assert memory.memory_type == "file"
            assert memory.file_path == file_path

    def test_persist_data(self):
        """Test data persistence across memory instances."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "persist_test.json")

            # Store data
            memory1 = Memory(memory_type="file", file_path=file_path)
            memory1.store("name", "Zhang San")
            memory1.store("score", 100)

            # Create new instance and verify data persists
            memory2 = Memory(memory_type="file", file_path=file_path)
            assert memory2.retrieve("name") == "Zhang San"
            assert memory2.retrieve("score") == 100

    def test_delete_persists(self):
        """Test delete operation persists to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "delete_test.json")

            memory1 = Memory(memory_type="file", file_path=file_path)
            memory1.store("key1", "value1")
            memory1.delete("key1")

            memory2 = Memory(memory_type="file", file_path=file_path)
            assert memory2.retrieve("key1") is None

    def test_clear_removes_file(self):
        """Test clear removes the file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "clear_test.json")

            memory = Memory(memory_type="file", file_path=file_path)
            memory.store("key", "value")
            assert os.path.exists(file_path)

            memory.clear()
            assert not os.path.exists(file_path)
            assert len(memory) == 0

    def test_file_not_exists_on_init(self):
        """Test memory initializes with empty data if file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "nonexistent.json")
            memory = Memory(memory_type="file", file_path=file_path)
            assert len(memory) == 0

    def test_invalid_json_file(self):
        """Test handling of invalid JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "invalid.json")

            # Create invalid JSON file
            with open(file_path, "w") as f:
                f.write("invalid json content {{{")

            # Memory should initialize with empty data
            memory = Memory(memory_type="file", file_path=file_path)
            assert len(memory) == 0


class TestMemoryIntegration:
    """Integration tests for Memory with other components."""

    def test_memory_with_list_values(self):
        """Test memory with list values (common use case)."""
        memory = Memory(memory_type="dict")

        # Store conversation history
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        memory.store("messages", messages)

        result = memory.retrieve("messages")
        assert len(result) == 2
        assert result[0]["role"] == "user"

    def test_memory_update_existing_key(self):
        """Test updating an existing key."""
        memory = Memory(memory_type="dict")

        memory.store("counter", 1)
        memory.store("counter", 2)
        memory.store("counter", 3)

        assert memory.retrieve("counter") == 3
        assert len(memory) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
