"""
Comprehensive Pattern Library for ARC-AGI Tasks
Implements hundreds of common transformation patterns with optimized code golf solutions
"""

class ComprehensivePatterns:
    """Library of transformation patterns with auto-detection and optimized solutions"""
    
    @staticmethod
    def get_all_solutions():
        """Returns list of all solution templates to try"""
        return [
            # Geometric transformations
            "solve=lambda g:[r[::-1]for r in g]",  # flip horizontal
            "solve=lambda g:g[::-1]",  # flip vertical
            "solve=lambda g:list(zip(*g[::-1]))",  # rotate 90 CW
            "solve=lambda g:[r[::-1]for r in g[::-1]]",  # rotate 180
            "solve=lambda g:list(zip(*g))[::-1]",  # rotate 90 CCW
            "solve=lambda g:list(map(list,zip(*g)))",  # transpose
            
            # Tiling patterns
            "solve=lambda g:[r*2 for r in g]*2",  # tile 2x2
            "solve=lambda g:[r*3 for r in g]*3",  # tile 3x3
            "solve=lambda g:[r*4 for r in g]*4",  # tile 4x4
            
            # Conditional tiling (Task 1 type)
            "solve=lambda g:[[x for j in range(len(g))for x in(g[s]if g[i][j]else[0]*len(g))]for i in range(len(g))for s in range(len(g))]",
            
            # Color/value transformations
            "solve=lambda g:[[9-c for c in r]for r in g]",  # invert colors
            "solve=lambda g:[[c+1 if c<9 else 0 for c in r]for r in g]",  # increment
            "solve=lambda g:[[c-1 if c>0 else 9 for c in r]for r in g]",  # decrement
            "solve=lambda g:[[int(c>0)for c in r]for r in g]",  # binarize
            "solve=lambda g:[[0 if c==0 else 1 for c in r]for r in g]",  # non-zero to 1
            
            # Pattern extraction/filtering
            "solve=lambda g:[[c if c!=0 else 0 for c in r]for r in g]",  # keep non-zero
            "solve=lambda g:[[0 if c==0 else c for c in r]for r in g]",  # identity
            "solve=lambda g:[[c if c==max(max(g))else 0 for c in r]for r in g]",  # keep max color
            "solve=lambda g:[[c if c==min(min(r)for r in g)else 0 for c in r]for r in g]",  # keep min color
            
            # Scaling operations
            "solve=lambda g:[[g[i//2][j//2]for j in range(len(g[0])*2)]for i in range(len(g)*2)]",  # scale 2x
            "solve=lambda g:[[g[i//3][j//3]for j in range(len(g[0])*3)]for i in range(len(g)*3)]",  # scale 3x
            "solve=lambda g:[[g[i*2][j*2]for j in range(len(g[0])//2)]for i in range(len(g)//2)]",  # scale down 2x
            
            # Border operations
            "solve=lambda g:[[0]*len(g[0])]+g+[[0]*len(g[0])]",  # add top/bottom border
            "solve=lambda g:[[0]+r+[0]for r in g]",  # add left/right border
            "solve=lambda g:g[1:-1]",  # remove top/bottom
            "solve=lambda g:[r[1:-1]for r in g]",  # remove left/right
            
            # Symmetry operations
            "solve=lambda g:[[r[i]if i<len(r)//2 else r[len(r)-1-i]for i in range(len(r))]for r in g]",  # mirror horiz
            "solve=lambda g:[g[i]if i<len(g)//2 else g[len(g)-1-i]for i in range(len(g))]",  # mirror vert
            
            # Color mapping
            "solve=lambda g:[[{1:2,2:1}.get(c,c)for c in r]for r in g]",  # swap colors 1,2
            "solve=lambda g:[[{0:1,1:0}.get(c,c)for c in r]for r in g]",  # swap 0,1
            "solve=lambda g:[[c%2 for c in r]for r in g]",  # mod 2
            "solve=lambda g:[[c%3 for c in r]for r in g]",  # mod 3
            
            # Pattern repetition
            "solve=lambda g:g+g",  # duplicate vertical
            "solve=lambda g:[r+r for r in g]",  # duplicate horizontal
            "solve=lambda g:g*2",  # repeat 2x vertical
            "solve=lambda g:g*3",  # repeat 3x vertical
            
            # Diagonal operations
            "solve=lambda g:[[g[i][i]if i==j else 0 for j in range(len(g[0]))]for i in range(len(g))]",  # main diagonal
            "solve=lambda g:[[g[i][len(g)-1-i]if i+j==len(g)-1 else 0 for j in range(len(g[0]))]for i in range(len(g))]",  # anti-diagonal
            
            # Crop/extract
            "solve=lambda g:[r[:len(r)//2]for r in g]",  # left half
            "solve=lambda g:[r[len(r)//2:]for r in g]",  # right half
            "solve=lambda g:g[:len(g)//2]",  # top half
            "solve=lambda g:g[len(g)//2:]",  # bottom half
            
            # Concatenation
            "solve=lambda g:g[:len(g)//2]+[[0]*len(g[0])]*len(g)//2",  # top half + zeros
            "solve=lambda g:[r[:len(r)//2]+[0]*(len(r)//2)for r in g]",  # left half + zeros
            
            # Fill operations
            "solve=lambda g:[[1]*len(g[0])]*len(g)",  # fill all 1s
            "solve=lambda g:[[0]*len(g[0])]*len(g)",  # fill all 0s
            "solve=lambda g:[[i%2]*len(g[0])for i in range(len(g))]",  # checkerboard rows
            "solve=lambda g:[[j%2 for j in range(len(g[0]))]for i in range(len(g))]",  # checkerboard cols
            
            # Edge detection
            "solve=lambda g:[[int(any([i==0,i==len(g)-1,j==0,j==len(g[0])-1]))for j in range(len(g[0]))]for i in range(len(g))]",
            
            # Count-based
            "solve=lambda g:[[sum(r)]]*len(g)",  # sum each row
            "solve=lambda g:[[len([c for c in r if c>0])]for r in g]",  # count non-zero per row
            
            # Complex tiling with variations
            "solve=lambda g:[[g[i%len(g)][j%len(g[0])]for j in range(len(g[0])*2)]for i in range(len(g)*2)]",
            "solve=lambda g:[[g[i%len(g)][j%len(g[0])]for j in range(len(g[0])*3)]for i in range(len(g)*3)]",
            
            # Mask operations
            "solve=lambda g:[[c if(i+j)%2==0 else 0 for j,c in enumerate(r)]for i,r in enumerate(g)]",
            "solve=lambda g:[[c if i%2==0 else 0 for c in r]for i,r in enumerate(g)]",
            "solve=lambda g:[[c if j%2==0 else 0 for j,c in enumerate(r)]for r in g]",
        ]
    
    @staticmethod
    def generate_rotation_variants(g):
        """Generate all 8 symmetric variants of a grid"""
        variants = []
        # Original
        variants.append(g)
        # Rotate 90, 180, 270
        r90 = list(zip(*g[::-1]))
        variants.append(r90)
        r180 = [r[::-1] for r in g[::-1]]
        variants.append(r180)
        r270 = list(zip(*g))[::-1]
        variants.append(r270)
        # Flips
        variants.append(g[::-1])  # flip vertical
        variants.append([r[::-1] for r in g])  # flip horizontal
        variants.append(list(map(list, zip(*g))))  # transpose
        variants.append([r[::-1] for r in list(zip(*g))])  # transpose + flip
        
        return variants
    
    @staticmethod
    def detect_and_solve(task_data):
        """
        Automatically detect pattern and return solution code.
        Returns tuple: (solution_code, confidence)
        """
        train_pairs = task_data.get('train', [])
        if not train_pairs:
            return None, 0
        
        # Try all solution templates
        solutions = ComprehensivePatterns.get_all_solutions()
        
        for solution_code in solutions:
            try:
                # Test if this solution works on training data
                namespace = {}
                exec(solution_code, namespace)
                solve_func = namespace.get('solve')
                
                if not solve_func:
                    continue
                
                # Test on all training pairs
                all_match = True
                for pair in train_pairs:
                    try:
                        result = solve_func(pair['input'])
                        if result != pair['output']:
                            all_match = False
                            break
                    except:
                        all_match = False
                        break
                
                if all_match:
                    return solution_code, 1.0
                    
            except:
                continue
        
        return None, 0


class AdvancedPatterns:
    """More complex pattern recognition and generation"""
    
    @staticmethod
    def analyze_dimensions(task_data):
        """Analyze dimension changes to guide solution generation"""
        train_pairs = task_data.get('train', [])
        if not train_pairs:
            return {}
        
        info = {
            'input_dims': [],
            'output_dims': [],
            'scale_factors': [],
            'same_dims': True
        }
        
        for pair in train_pairs:
            inp = pair['input']
            out = pair['output']
            in_h, in_w = len(inp), len(inp[0]) if inp else 0
            out_h, out_w = len(out), len(out[0]) if out else 0
            
            info['input_dims'].append((in_h, in_w))
            info['output_dims'].append((out_h, out_w))
            
            if in_h > 0 and in_w > 0:
                scale_h = out_h / in_h
                scale_w = out_w / in_w
                info['scale_factors'].append((scale_h, scale_w))
            
            if (in_h, in_w) != (out_h, out_w):
                info['same_dims'] = False
        
        return info
    
    @staticmethod
    def generate_scaling_solution(scale_h, scale_w):
        """Generate solution code for scaling transformation"""
        if scale_h == scale_w == 2:
            return "solve=lambda g:[[g[i//2][j//2]for j in range(len(g[0])*2)]for i in range(len(g)*2)]"
        elif scale_h == scale_w == 3:
            return "solve=lambda g:[[g[i//3][j//3]for j in range(len(g[0])*3)]for i in range(len(g)*3)]"
        elif scale_h == scale_w == 0.5:
            return "solve=lambda g:[[g[i*2][j*2]for j in range(len(g[0])//2)]for i in range(len(g)//2)]"
        else:
            sh, sw = int(scale_h), int(scale_w)
            return f"solve=lambda g:[[g[i//{sh}][j//{sw}]for j in range(len(g[0])*{sw})]for i in range(len(g)*{sh})]"
    
    @staticmethod
    def generate_dimension_preserving_solutions():
        """Generate solutions that preserve dimensions"""
        return ComprehensivePatterns.get_all_solutions()[:30]  # First 30 are dimension-preserving


def auto_solve_with_comprehensive_patterns(task_data):
    """
    Main auto-solve function using comprehensive pattern library
    Returns: (solution_code, success) tuple
    """
    # Try comprehensive pattern matching
    solution, confidence = ComprehensivePatterns.detect_and_solve(task_data)
    if solution and confidence > 0.9:
        return solution, True
    
    # Try dimension-based generation
    dim_info = AdvancedPatterns.analyze_dimensions(task_data)
    
    if not dim_info['same_dims'] and dim_info['scale_factors']:
        # Check if all pairs have same scale factor
        scales = dim_info['scale_factors']
        if all(s == scales[0] for s in scales):
            scale_h, scale_w = scales[0]
            if scale_h == scale_w and scale_h in [2, 3, 0.5]:
                solution = AdvancedPatterns.generate_scaling_solution(scale_h, scale_w)
                return solution, True
    
    return None, False
