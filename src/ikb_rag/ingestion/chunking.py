"""Structural element chunking strategies with page context preservation.

Splits MinerU parsed output into isolated vectors for text, tables, equations,
and technical diagrams while linking full page context.
"""

import os
from typing import Dict, Any, List, Tuple
from config.settings import API_PORT


class StructuralElementChunker:
    """Chunks documents into granular elements while maintaining full parent page context."""

    def __init__(self, api_port: int = API_PORT):
        self.api_port = api_port

    def chunk(
        self,
        parsed_data: Any,
        text: str,
        chat_id: str,
        base_name: str,
        pdf_base: str,
        doc_url: str
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        """Performs two-pass structural element chunking with fallback.
        
        Returns:
            Tuple of (raw_elements_for_embedding, payloads_for_storage)
        """
        print("🟡 Build outputs: Structural Element Chunking (with Page Context)...")
        raw_elements = []
        payloads = []

        page_contents: Dict[int, str] = {}

        content_list = []
        if isinstance(parsed_data, dict) and "data" in parsed_data and "content_list" in parsed_data["data"]:
            content_list = parsed_data["data"]["content_list"]
        elif isinstance(parsed_data, list):
            content_list = parsed_data

        # First Pass: Build the full_page_context for every page
        for block in content_list:
            p_idx = block.get("page_idx", 0)
            b_type = block.get("type")

            if b_type in ["header", "footer", "page_number"]:
                continue
            if p_idx not in page_contents:
                page_contents[p_idx] = ""

            if b_type == "text":
                page_contents[p_idx] += block.get("text", "") + "\n\n"
            elif b_type == "table":
                page_contents[p_idx] += block.get("table_body", block.get("text", "")) + "\n\n"
            elif b_type == "equation":
                page_contents[p_idx] += block.get("equation_body", block.get("text", "")) + "\n\n"
            elif b_type == "image":
                img_path = block.get("img_path", "")
                img_filename = os.path.basename(img_path)
                img_url = f"http://localhost:{self.api_port}/images/{chat_id}/{pdf_base}/{img_filename}"
                cap = block.get("image_caption", "")
                caption = " ".join(cap) if isinstance(cap, list) else str(cap)
                foot = block.get("image_footnote", "")
                footnote = " ".join(foot) if isinstance(foot, list) else str(foot)
                img_md = f"![{caption.strip()}]({img_url})"
                if footnote.strip():
                    img_md += f"\n*{footnote.strip()}*"
                page_contents[p_idx] += img_md + "\n\n"

        # Second Pass: Create isolated vectors for every structural element
        for block in content_list:
            p_idx = block.get("page_idx", 0)
            b_type = block.get("type")

            if b_type in ["header", "footer", "page_number"]:
                continue

            element_content_for_llm = ""
            element_content_for_embedding = ""

            if b_type == "text":
                element_content_for_llm = block.get("text", "")
                element_content_for_embedding = element_content_for_llm
            elif b_type == "table":
                element_content_for_llm = block.get("table_body", block.get("text", ""))
                element_content_for_embedding = element_content_for_llm
            elif b_type == "equation":
                element_content_for_llm = block.get("equation_body", block.get("text", ""))
                element_content_for_embedding = element_content_for_llm
            elif b_type == "image":
                img_path = block.get("img_path", "")
                img_filename = os.path.basename(img_path)
                img_url = f"http://localhost:{self.api_port}/images/{chat_id}/{pdf_base}/{img_filename}"
                cap = block.get("image_caption", "")
                caption = " ".join(cap) if isinstance(cap, list) else str(cap)
                foot = block.get("image_footnote", "")
                footnote = " ".join(foot) if isinstance(foot, list) else str(foot)

                element_content_for_llm = f"![{caption.strip()}]({img_url})"
                if footnote.strip():
                    element_content_for_llm += f"\n*{footnote.strip()}*"

                element_content_for_embedding = f"Image Diagram Figure: {caption.strip()} {footnote.strip()}"

            if not element_content_for_embedding.strip():
                continue

            actual_page = p_idx + 1
            page_fragment = f"#page={actual_page}"
            unique_page_id = f"{chat_id}_{base_name}_page_{actual_page}"

            formatted_element = f"Element Matched: {element_content_for_llm.strip()}"
            full_page_text = page_contents.get(p_idx, '').strip()

            raw_elements.append(element_content_for_embedding.strip())

            payloads.append({
                "chat_id": chat_id,
                "page_id": unique_page_id,
                "source_file": base_name,
                "page_num": actual_page,
                "link": f"{doc_url}{page_fragment}",
                "matched_element": formatted_element,
                "parent_context": full_page_text
            })

        # Fallback if content_list was empty
        if not raw_elements and text.strip():
            for i in range(0, len(text), 1500):
                chunk = text[i:i + 1500]
                raw_elements.append(chunk)
                payloads.append({
                    "chat_id": chat_id,
                    "page_id": f"{chat_id}_{base_name}_fallback_{i}",
                    "source_file": base_name,
                    "page_num": "?",
                    "link": f"{doc_url}",
                    "matched_element": f"Element Matched: {chunk}",
                    "parent_context": chunk
                })

        return raw_elements, payloads
