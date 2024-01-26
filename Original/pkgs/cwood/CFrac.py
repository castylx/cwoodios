from fractions import Fraction

class CFrac (Fraction):
    
    ###############################################################
    # Takes a Frac object and returns the string representation
    ################################################################
    def __str__(self):
        res = "UNKNOWN : Contact Developer"

        n = self.numerator
        d = self.denominator
        
        whole = int(n/d)
        awhole = abs(whole) # Get absolute value

        # Let's get the left over Frac
        if (awhole > 0):
            frac = abs(n) - (awhole * d)
            if (frac == 0):
                res = "{}".format(whole)
            else:
                res = "{} {}/{}".format(whole, frac, d)
        else:
            res = "{}/{}".format(n, d)

        return res

