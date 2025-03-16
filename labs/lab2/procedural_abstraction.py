class ProceduralAbstraction:
    """
    A class that contains methods to perform specific mathematical and matrix operations.
    
    Methods:
        reverse_factorial(x): Returns the smallest positive integer n such that n! is 
            greater than or equal to x (if x > 0). For x <= 0, returns 1.
        is_matrix_nice(matrix): Checks if the given square matrix is "nice" (i.e. all row 
            sums, column sums, and both diagonal sums are equal). If so, prints the sum and 
            returns True; otherwise returns False.
    """

    @staticmethod
    def reverse_factorial(x: int) -> int:
        """
        For a positive integer x, this method returns the smallest positive integer n
        for which n! is greater than or equal to x. If x is not positive, it returns 1.

        """
        hold = x
        divider = 1

        if x > 0:
            # Loop until the integer division result drops to 1 or below.
            while hold > 1:
                hold = hold // divider
                divider += 1
            answer = divider - 1
        else:
            answer = 1

        return answer

    @staticmethod
    def is_matrix_nice(matrix: list[list[int]]) -> bool:
        """
        Determines if a square matrix is "nice" (all row sums, column sums, and both diagonal 
        sums are equal). If it is nice, the method prints the sum and returns True; otherwise, 
        returns False.
        
        The algorithm:
          1. Check if the matrix is square.
          2. Compute the sums of each row, each column, and the two diagonals.
          3. Confirm that all these sums are equal.
          
        """
        row_size = len(matrix)
        if row_size == 0 or any(len(row) != row_size for row in matrix):
            return False  # not a square matrix
        
        # Calculate row sums and column sums
        row_sums = [sum(row) for row in matrix]
        col_sums = [sum(matrix[i][j] for i in range(row_size)) for j in range(row_size)]
        
        # Calculate both diagonal sums
        diag1_sum = sum(matrix[i][i] for i in range(row_size))
        diag2_sum = sum(matrix[i][row_size - i - 1] for i in range(row_size))
        
        # Check if all sums are equal. Using set makes it easy to check uniqueness.
        all_sums = set(row_sums + col_sums + [diag1_sum, diag2_sum])
        if len(all_sums) == 1:
            print(f"The sum is: {diag1_sum}")
            return True
        else:
            return False


# Main block to execute the functionality when the module is run directly.
if __name__ == '__main__':
    # A sample magic square matrix
    matrix = [
        [2, 7, 6],
        [9, 5, 1],
        [4, 3, 8]
    ]
    
    result = ProceduralAbstraction.is_matrix_nice(matrix)
    print(result)
    
    print(ProceduralAbstraction.reverse_factorial(1000))