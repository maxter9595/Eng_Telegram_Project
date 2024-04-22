def hello_text() -> str:
        
        text = """
        Привет 👋 Давай попрактикуемся в английском языке.
        
        Тренировки можешь проходить в удобном для себя темпе.
        
        Для этого воспрользуйся следующимим инструментами:
        добавить слово ➕,
        удалить слово 🔙.

        Ну что, начнём ⬇️
        """
        
        return '\n'.join(
                        line.lstrip() 
                        for line in text.splitlines()
                )


def show_hint(*lines:tuple) -> str:
        
        return '\n'.join(
                        lines
                )


def show_target(data:dict) -> str:
        
        target = data['target_word']
        trans = data['translate_word']
        
        return f"{target} -> {trans}"