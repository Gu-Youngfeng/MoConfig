package cn.edu.whu.cstar.mosampling.moea;

import java.io.File;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import org.moeaframework.Executor;
import org.moeaframework.core.NondominatedPopulation;
import org.moeaframework.core.Problem;
import org.moeaframework.core.Solution;
import org.moeaframework.core.variable.EncodingUtils;
import cn.edu.whu.cstar.experiments.ResultsDataCenter;
import cn.edu.whu.cstar.experiments.ResultsNode;
import cn.edu.whu.cstar.mosampling.moea.MoConfigProblem;
import cn.edu.whu.cstar.mosampling.moea.MoConfigProblem.ObjectiveName;
import cn.edu.whu.cstar.mosampling.tool.FileReaderWriter;
import cn.edu.whu.cstar.mosampling.moea.InstanceReader;

/**
 * <p>Running MOEA Framework with different Objective combinations</p>
 * @author jifeng
 * @update 2019.10.5
 */
public class XMoeaProcessor {
	/** number of trial using MOEA*/
	static int numTrial = 30;
	/** number of stop criteria*/
	static int numMaxEval = 10000;
	
	/** List of Multi-objective Evolutionary Algorithms: "NSGAII", "DBEA", "eMOEA", "IBEA" */
	final static String[] arrayAlgorithm = {"NSGAII"};
//	final static String[] arrayAlgorithm = {"NSGAII", "DBEA", "eMOEA", "IBEA" };
	
	/** Length of arrayAlgorithm*/
	final static int numAlgo = arrayAlgorithm.length;
	
	int numTotalDetectedFault = -1;
	/** Objective A*/
	ObjectiveName objectiveA; 
	/** Objective B*/
	ObjectiveName objectiveB;
	
	private List<String> listLineInPath = null;
	
	private String outFolder = null;
	private String inFileName = null;
	
	/***
	 * <p>To evaluate the Genetic Algorithm on a .csv file using objective A and B.</p>
	 * @param nTrial repeat time of experiment
	 * @param nMaxEval number of loops
	 * @param inPathInstance path of .csv file
	 * @param outFolder output directory
	 * @param objA objective A
	 * @param objB objective B
	 */
	public void evaluateAll(int nTrial, int nMaxEval, String inPathInstance, String outFolder, ObjectiveName objA, ObjectiveName objB) {
		numTrial = nTrial;
		numMaxEval = nMaxEval;
		
		objectiveA = objA;
		objectiveB = objB;
		
		String projName = inPathInstance.substring(inPathInstance.lastIndexOf("/")+1,inPathInstance.lastIndexOf("_")); // project name
		this.outFolder = outFolder + projName + "/";
//		System.out.print(this.outFolder);
		File outFolderDir = new File(this.outFolder);
		outFolderDir.mkdir();
		
		File inFile = new File(inPathInstance);
		if(inFile.exists()) {
			inFileName = inFile.getName(); // get the name of .csv file
		}
		
		listLineInPath = FileReaderWriter.readFileByLine(inPathInstance); // save content of .csv file in {$listLineInPath}
		
		for(int i = 0; i < numTrial; i ++) {
			for(String algoName: arrayAlgorithm) { // for each algorithm
				evaluateEffectivenessForOne(inPathInstance, algoName, i);
			}	
		}
	}
	
	private void evaluateEffectivenessForOne(String inPath, String algoName, int indexTrial) {
		// read instance from inPath
		InstanceReader instances = new InstanceReader(inPath);
		// define the moea problem
		Problem problem = new MoConfigProblem(instances, objectiveA, objectiveB);
		// get the project name
		String projName = inPath.substring(inPath.lastIndexOf("/")+1,inPath.lastIndexOf("_")); // project name
		
		NondominatedPopulation population = new Executor() //  to execute an algorithm on a specific problem
			       .withAlgorithm(algoName) // algorithm name
			       .withProblem(problem) // setting of objective, chromosome, 
			       .withMaxEvaluations(numMaxEval) // loop times: 10000
			       .run();
		
		Iterator<Solution> iterator = population.iterator(); // print the Pareto Front
		
		List<Double> listObj1 = new ArrayList<Double>();
		List<Double> listObj2 = new ArrayList<Double>();
		
		while(iterator.hasNext()) {
			Solution solution = iterator.next();
	
			double valueObj0 = solution.getObjective(0); // 1-st objective value of solution, i.e., numSamples
			double valueObj1 = solution.getObjective(1); // 2-nd objective value of solution, i.e., entropy, density, or variance
			
			String fileName = String.format("%s_%s_%s_%s_%d_%f", inFileName, objectiveA.toString(), objectiveB.toString(), algoName, indexTrial, valueObj0);
			
			selectConfigsBySolution(solution, fileName);
			
			listObj1.add(valueObj0);
			listObj2.add(valueObj1);
		}
		
		// save solutions and their objective values into the static class ResultsDataCenter
		ResultsNode node = new ResultsNode(projName, algoName, objectiveA, objectiveB);
		node.saveResults(listObj1, listObj2);
		ResultsDataCenter.addData(node);
	}
	
	/** <p>Select the configurations by the solution, then save the selected configurations into a output file.</p>
	 *  <p>Note that, the "1" and "0" in solution denote the "select" and "not select" the configurations at that position.</p>
	 * */
	private void selectConfigsBySolution(Solution solution, String fileName) {
		// Returns a new binary decision variable with X of bits.
		boolean[] x = EncodingUtils.getBinary(solution.getVariable(0));
		
		List<String> listLine = new ArrayList<String>();
		
		listLine.add(listLineInPath.get(0)); // features in csv file
		
		for(int i = 0; i < x.length; i ++)
		{
			if(x[i]) // if x[i] = 1, then select the i-th configuration in ${listLineInPath}.
				listLine.add(listLineInPath.get(i + 1));
		}
		
		String outPath = String.format("%s/%s.csv", outFolder, fileName);
		FileReaderWriter.writeFileByLine(outPath, listLine);  // output the selected configurations of ${fileName}
	}

}
