"""
Enhanced pattern library with more ARC transformation types.
"""

class EnhancedPatterns:
    """Extended pattern solutions for better coverage."""
    
    # Core patterns (fixed syntax)
    TASK1 = "solve=lambda g:[[x for j in range(3)for x in(g[s]if g[i][j]else[0]*3)]for i in range(3)for s in range(3)]"
    ROTATE_90 = "solve=lambda g:[list(r)for r in zip(*g[::-1])]"
    ROTATE_180 = "solve=lambda g:[r[::-1]for r in g[::-1]]"
    FLIP_H = "solve=lambda g:[r[::-1]for r in g]"
    FLIP_V = "solve=lambda g:g[::-1]"
    TRANSPOSE = "solve=lambda g:[list(r)for r in zip(*g)]"
    IDENTITY = "solve=lambda g:g"
    
    # Tiling patterns
    TILE_2X2 = "solve=lambda g:[r*2for r in g]*2"
    TILE_3X3 = "solve=lambda g:[r*3for r in g]*3"
    
    # Color operations
    INVERT_COLORS = "solve=lambda g:[[9-c for c in r]for r in g]"
    ZERO_NONZERO = "solve=lambda g:[[0 if c else 1 for c in r]for r in g]"
    EXTRACT_COLOR = "solve=lambda g:[[c if c==max(sum(g,[]))else 0 for c in r]for r in g]"
    
    # Size operations
    SCALE_2X = "solve=lambda g:sum([[[c]*2 for c in r]*2 for r in g],[])"
    SHRINK_2X = "solve=lambda g:[r[::2]for r in g[::2]]"
    
    # Pattern detection
    FILL_ZEROS = "solve=lambda g:[[1 if c==0 else c for c in r]for r in g]"
    OUTLINE_ONLY = "solve=lambda g:[[g[i][j]if i==0 or i==len(g)-1 or j==0 or j==len(r)-1 else 0 for j,c in enumerate(r)]for i,r in enumerate(g)]"
    
    @classmethod
    def get_all_patterns(cls):
        """Get all pattern solutions."""
        return [
            cls.TASK1, cls.ROTATE_90, cls.ROTATE_180, cls.FLIP_H, cls.FLIP_V,
            cls.TRANSPOSE, cls.TILE_2X2, cls.TILE_3X3, cls.INVERT_COLORS,
            cls.ZERO_NONZERO, cls.EXTRACT_COLOR, cls.SCALE_2X, cls.SHRINK_2X,
            cls.FILL_ZEROS, cls.OUTLINE_ONLY, cls.IDENTITY
        ]