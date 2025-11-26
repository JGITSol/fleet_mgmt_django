import re
from pathlib import Path

def clean_po_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    output_lines = []
    seen_msgids = set()
    
    current_block = []
    current_msgid = None
    current_is_obsolete = False
    is_header = True
    
    for line in lines:
        # Check if line starts a new block (msgid that is NOT a comment)
        # But wait, comments belong to the following msgid.
        # So a block ends when we see a new msgid line, OR when we see comments after a msgstr?
        # Standard PO: 
        # # comments
        # msgid "..."
        # msgstr "..."
        # \n
        
        # We can accumulate lines until we hit a `msgid` line.
        # When we hit `msgid`, we parse the PREVIOUS block.
        
        if line.startswith('msgid "'):
            # This is the start of the identifier part of a block.
            # But we might have collected comments for this block already in `current_block`.
            # Actually, let's process the file by splitting on blank lines? No, blank lines are not reliable.
            pass
            
    # Let's try a different approach:
    # Read the whole file.
    # Split by `\n\n` is risky because msgstr can contain `\n\n`.
    
    # Regex approach:
    # Find all blocks that look like:
    # (comments)*
    # msgid "..."
    # (msgid_plural "...")?
    # msgstr "..."
    
    # But we want to preserve structure.
    
    # Simplest approach for THIS specific issue:
    # The duplicates are at the end of the file.
    # We can just read the file, find all `msgid "..."` lines.
    # If we see a `msgid` that we've seen before (active, not commented), we mark this block for deletion.
    
    # But we need to know where the block starts and ends.
    
    # Let's use a state machine.
    
    processed_blocks = [] # List of (msgid, lines)
    
    current_lines = []
    current_msgid = None
    
    for line in lines:
        stripped = line.strip()
        
        # If we hit a line that looks like the start of a new entry (comment or msgid)
        # AND we have finished a previous entry (seen msgstr).
        # This is hard to parse perfectly without a real parser.
        
        # HEURISTIC:
        # If line starts with `msgid "`, it's the key.
        # If we are currently in a block and hit `msgid "` again, it's a new block (unless it's multiline msgid? No, multiline is `msgid "..." \n "..."`)
        
        # Check for msgid (active or obsolete)
        # Obsolete entries start with #~ followed by whitespace and msgid
        match = re.search(r'^(?:#~\s*)?msgid "([^"]*)"', line)
        
        if match:
            # If we have a current block, save it
            if current_lines:
                # Check if the previous block had a msgid
                if current_msgid:
                    processed_blocks.append({'msgid': current_msgid, 'lines': current_lines, 'is_obsolete': current_is_obsolete})
                else:
                    # Header or comments without msgid
                    processed_blocks.append({'msgid': None, 'lines': current_lines, 'is_obsolete': False})
                
            current_lines = [line]
            current_msgid = match.group(1)
            current_is_obsolete = line.strip().startswith('#~')
            print(f"Found msgid: {current_msgid} (Obsolete: {current_is_obsolete})")
        else:
            current_lines.append(line)
            
    # Append last block
    if current_lines:
        processed_blocks.append({'msgid': current_msgid, 'lines': current_lines, 'is_obsolete': current_is_obsolete})
        
    print(f"Total blocks found: {len(processed_blocks)}")
    
    final_blocks = []
    msgid_to_index = {}
    
    for block in processed_blocks:
        mid = block['msgid']
        if mid is not None:
            if mid == "": # Header
                final_blocks.append(block)
                continue
                
            if mid in msgid_to_index:
                # Duplicate found!
                print(f"Duplicate found: {mid}")
                old_index = msgid_to_index[mid]
                old_block = final_blocks[old_index]
                
                # Decision logic:
                # If new block is active and old is obsolete -> Replace
                # If new block is active and old is active -> Replace (assume newer is better)
                # If new block is obsolete and old is active -> Keep old
                # If new block is obsolete and old is obsolete -> Replace (assume newer is better)
                
                if not block['is_obsolete']:
                    # New is active, always replace
                    final_blocks[old_index] = block
                elif old_block['is_obsolete']:
                    # Both obsolete, replace
                    final_blocks[old_index] = block
                else:
                    # New is obsolete, old is active -> Keep old
                    pass
            else:
                final_blocks.append(block)
                msgid_to_index[mid] = len(final_blocks) - 1
        else:
            # Block without msgid (e.g. detached comments), just keep it
            final_blocks.append(block)
            
    # Reconstruct file
    with open(file_path, 'w', encoding='utf-8') as f:
        for block in final_blocks:
            f.writelines(block['lines'])
            
    return len(processed_blocks) - len(final_blocks)

if __name__ == "__main__":
    base_dir = Path(r'd:\REPOS\fleet_mgmt_django\locale')
    languages = ['de', 'fr', 'es', 'pl', 'en']
    
    for lang in languages:
        po_file = base_dir / lang / 'LC_MESSAGES' / 'django.po'
        if po_file.exists():
            removed = clean_po_file(po_file)
            print(f"Cleaned {lang}: removed {removed} duplicates")
