package cn.edu.whu.cstar.mosampling.moea;

import java.util.LinkedList;
import java.util.List;

import org.moeaframework.core.Solution;
import org.moeaframework.core.variable.BinaryVariable;
import org.moeaframework.core.variable.EncodingUtils;
import org.moeaframework.problem.AbstractProblem;


/**
 * <p>Definition of the moea problem extended from the AbstractProblem.
 * If you have to add new objective then you add code at MOD-1, MOD-2, MOD-3.
 * </p>
 * @author jifeng
 * @update 2019.10.5
 */
public class MoConfigProblem extends AbstractProblem {
	

	public enum ObjectiveName {
			NUMSAMPLE, ENTROPY, VARIANCE, DENSITY,
			/** MOD-1: add new objective name here*/
	}
	
	public static int NUM_VARIABLE = 1; // 1 variable with numFitness bits. 
	/** number of objective: 2*/
	public final static int NUM_OBJECTIVE = 2;
	public final static double LOG_E2= Math.log(2);
	/** maximum int: 10000*/
	public final static int MAX_INT = 10000;
	
	private ObjectiveName objectiveA = null;
	private ObjectiveName objectiveB = null;
		
//	public final static double SMOOTH_FACTOR = 0.000001;
		
	private InstanceReader inst = null;
	private int numOption = -1;
	private int numConfiguration = -1;

	/**
	 * Constructs a new instance 
	 * 
	 * {@code indexObjectiveA} and {@code indexObjectiveB} are the indexes of two objectives. 
	 */
	public MoConfigProblem(InstanceReader inst, ObjectiveName objectiveA, ObjectiveName objectiveB) {
		super(1, NUM_OBJECTIVE);
		this.objectiveA = objectiveA;
		this.objectiveB = objectiveB;
		this.inst = inst;
		
		this.numOption = inst.numOption;
		this.numConfiguration = inst.numConfiguration;
	}

	/**
	 * The newSolution method defines the problem representation (the number and types of its decision variables). <br><br>
	 * Constructs a new solution and defines the bounds of the decision variables.
	 * Solution is a bitvector, i.e., each requirement is related to true or false.
	 * Here, the solution is just one bitvector with {@code numConfiguration} bits.  
	 */
	@Override
	public Solution newSolution() {
		Solution solution = new Solution(getNumberOfVariables(), getNumberOfObjectives());
	
		solution.setVariable(0, new BinaryVariable(inst.numConfiguration)); // initialize the 1-st decision variable for binary strings.
//		for (int i = 0; i < getNumberOfVariables(); i++)	// num_var = 1; 
//			solution.setVariable(i, new BinaryVariable(inst.numConfiguration));
		
		return solution;
	}
	
	/**
	 * Extracts the decision variables from the solution 
	 */
	@Override
	public void evaluate(Solution solution) {
		// Object 0, number of detected faults
		boolean[] arrayHitFlag = new boolean[inst.numConfiguration];
		for(int j = 0; j < inst.numConfiguration; j ++) {
			arrayHitFlag[j] = false;
		}
				
		double objA = evaluateObjective(solution, objectiveA); // get the objective A of solution
		if(objA == 0) {
			objA = MAX_INT;
		}
		
		double objB = evaluateObjective(solution, objectiveB); // get the objective B of solution
		if(objB == 0) {
			objB = MAX_INT;
		}
		
		double[] arrayObjResult = {objA, objB}; // objective set
		
		solution.setObjectives(arrayObjResult);
	}

	private double evaluateObjective(Solution solution, ObjectiveName objectiveName) {
		double result = 0;
		
		BinaryVariable variable = (BinaryVariable) solution.getVariable(0); // return the variable at index 0.
		int numHit = variable.cardinality(); // return the number of bit to true
		boolean[] x = null;
		
		switch(objectiveName) {
		case NUMSAMPLE:
			result = numHit;
			break;			
		case ENTROPY:
			x = EncodingUtils.getBinary(solution.getVariable(0)); // binary bit
			result = calcEntropy(x, numHit);
			break;			
		case VARIANCE:
			x = EncodingUtils.getBinary(solution.getVariable(0));
			result = calcVariance(x, numHit);
			break;
		case DENSITY:
			x = EncodingUtils.getBinary(solution.getVariable(0));
			result = calcDenity(x, numHit);	
			break;	
		/** MOD-2: add new objective case here*/
		default:
			System.out.println("Error, the program should not reach here.");
			break;
		}
		
		return result;
	}

	
	/**
	 * <p>Evaluation of the objective Entropy, i.e., the sum of variance of selected configurations</p>
	 * <pre>
	 * 10000 - sum(entropy_j) where entropy_j is the entropy of Option j
	 * entropy_j = E(-log_2(P(X_j))) = -sum_{x_ij \in X_j} P(x_ij)log(P(x_ij)), where x_ij is the i-th value of Option j
	 * </pre>
	 * @param x
	 * @param numHit
	 * @return 
	 * 	
	 */
	private double calcEntropy(boolean[] x, int numHit) {
		if(numHit == 0)
			return MAX_INT;
		
		List<Double> listValue = new LinkedList<Double>();
		List<Double> listCount = new LinkedList<Double>(); 

		double value = -1;
		
		double result = 0;
		for(int j = 0; j < numOption; j ++) {
			// Option j
			listValue.clear();
			listCount.clear();
			
			for(int i = 0; i < numConfiguration; i ++) {
				if(x[i]) {
					value = inst.matrixValue[i][j]; // value = 1
					int sizeList = listValue.size();
					int k = 0;
					for( ; k < sizeList; k ++) {
						if(value < listValue.get(k)) {
							listValue.add(k, value);
							listCount.add(k, 1.0);
							break;
						}
						else if(value == listValue.get(k)) {
							listCount.set(k, listCount.get(k) +1);
							break;
						}
//						else //   >
					}
					
					if(k >= sizeList) {
						listValue.add(sizeList, value);
						listCount.add(sizeList, 1.0);
					}
				}
			}
			
			double resultForOneOption = 0;
			
			for(int k = 0; k < listCount.size(); k ++) {
				double prob = listCount.get(k) / numHit;
				resultForOneOption += prob * getLog2(prob);
			}
			
			result += (0 - resultForOneOption);
		}
		
		return MAX_INT - result;
	}
	
	/**
	 * <p>Evaluation of the objective Variance, i.e., the sum of variance of selected configurations</p>
	 * @param x
	 * @param numHit
	 * @return sum(EuclDist(ConfigX - ConfigAvg))
	 */
	private double calcVariance(boolean[] x, int numHit) {
		if(numHit == 0)
			return MAX_INT;
		
		double result = 0;
		
		double[] arrayMin = new double[numOption];
		double[] arrayMax = new double[numOption];
		double[] arrayAvg = new double[numOption];
		
		double value = -1;
		
		for(int j = 0; j < numOption; j ++) {
			arrayMin[j] = Double.MAX_VALUE;
			arrayMax[j] = Double.MIN_VALUE;
			arrayAvg[j] = 0;
		}
		
		for(int i = 0; i < numConfiguration; i ++) {
			if(x[i]) {
				for(int j = 0; j < numOption; j ++) {
					value = inst.matrixValue[i][j];
					if(value < arrayMin[j])
						arrayMin[j] = value;
					if(value > arrayMax[j])
						arrayMax[j] = value;

					arrayAvg[j] += value;
				}	
			}
		}
		
		for(int j = 0; j < numOption; j ++) {
			arrayAvg[j] = arrayAvg[j] / numHit;
			arrayMin[j] = arrayMax[j] - arrayMin[j];
		}
		
		
		double resultSub = -1;
		for(int i = 0; i < numConfiguration; i ++) {
			resultSub = 0;
			if(x[i]) {
				for(int j = 0; j < numOption; j ++)	{
					value = inst.matrixValue[i][j];
				
					if(arrayMin[j] == 0)	// All values are the same. 
						value = 1;
					else
						value = (value - arrayAvg[j]) / arrayMin[j];
					
					resultSub += value * value; 
				}	
			}
			
			result += resultSub;
		}
				
		return MAX_INT - result; 
	}
	
	/**
	 * <p>Evaluation of the objective Density.</p>
	 * @param x
	 * @param numHit
	 * @return 
	 */
	private double calcDenity(boolean[] x, int numHit) {
		if(numHit == 0)
			return MAX_INT;
		
		List<Double> listValue = new LinkedList<Double>();

		double value = -1;
		
		double result = 0;
		for(int j = 0; j < numOption; j ++) {
			// Option j
			listValue.clear();
			
			for(int i = 0; i < numConfiguration; i ++) {
				if(x[i]) {
					value = inst.matrixValue[i][j];
					
					if(! listValue.contains(value))
						listValue.add(value);
				}
			}
			
			result += listValue.size();
		}
		
		result = result / (numOption * numHit);
		
		return MAX_INT - result;
	}
	
	private double getLog2(double val) {
		return Math.log(val) / LOG_E2;
	}
	
	/** MOD-3: add new objective evaluation here*/
}
