package cn.edu.whu.cstar.mosampling.moea;


import java.io.File;
//import java.io.IOException;
//import java.lang.reflect.Array;
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
import cn.edu.whu.cstar.mosampling.moea.MOEA;
import cn.edu.whu.cstar.mosampling.moea.MOEA.ObjectiveName;
import cn.edu.whu.cstar.mosampling.tool.FileReaderWriter;
import cn.edu.whu.cstar.mosampling.moea.MOEAInstance;


public class XMoeaProcessor {
	
	static int numTrial = 30;
	static int numMaxEval = 10000;
	/** List of Multi-objective GA algorithms: "NSGAII", "DBEA", "eMOEA", "IBEA" */
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
	public void evaluateAll(int nTrial, int nMaxEval, String inPathInstance, String outFolder, ObjectiveName objA, ObjectiveName objB)
	{
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
		if(inFile.exists())
			inFileName = inFile.getName(); // get the name of .csv file
		
//		String line = String.format("#Trial: %d\t#Eval: %d\tObjetiveA: %s\tObjectiveB: %s\n", numTrial, numMaxEval, objectiveA.toString(), objectiveB.toString());
//		System.out.println(line); // print each parameter 
		
		listLineInPath = FileReaderWriter.readFileByLine(inPathInstance); // save the line list of .csv file in {$listLineInPath}
		
		
		for(int i = 0; i < numTrial; i ++)
		{
			for(String algoName: arrayAlgorithm) // for each algorithm
			{
//				System.out.println(String.format("%s\tTrialID: %d", algoName, i));
				evaluateEffectivenessForOne(inPathInstance, algoName, i);
			}	
		}
	}
	
	private void evaluateEffectivenessForOne(String inPath, String algoName, int indexTrial)
	{
		MOEAInstance instance = new MOEAInstance(inPath);
		Problem problem = new MOEA(instance, objectiveA, objectiveB);
//		System.out.println(inPath);
		String projName = inPath.substring(inPath.lastIndexOf("/")+1,inPath.lastIndexOf("_")); // project name
		
		NondominatedPopulation population = new Executor() //  to execute an algorithm on a specific problem
			       .withAlgorithm(algoName) // algorithm name
			       .withProblem(problem) // setting of objective, chromosome, 
			       .withMaxEvaluations(numMaxEval) // loop times: 10000
			       .run();
		
		Iterator<Solution> iterator = population.iterator(); // print the Pareto Front
		
		List<Double> listObj1 = new ArrayList<Double>();
		List<Double> listObj2 = new ArrayList<Double>();
		
		while(iterator.hasNext())
		{
			Solution solution = iterator.next();
	
			double obj0 = solution.getObjective(0);
			double obj1 = solution.getObjective(1);
			
			String fileName = String.format("%s_%s_%s_%s_%d_%f", inFileName, objectiveA.toString(), objectiveB.toString(), algoName, indexTrial, obj0);
			
//			System.out.println(
//					String.format("%f\t%f\t%s", obj0, obj1, fileName)
//					);
			
			printFile(solution, fileName);
			
			listObj1.add(obj0);
			listObj2.add(obj1);
		}
		
		// save solutions and their objective values into static class ResultsDataCenter
		ResultsNode node = new ResultsNode(projName, algoName, objectiveA, objectiveB);
		node.saveResults(listObj1, listObj2);
		ResultsDataCenter.addData(node);
	}
	
	/** to save all the chromosomes into the .csv file*/
	private void printFile(Solution solution, String fileName)
	{
		boolean[] x = EncodingUtils.getBinary(solution.getVariable(0));
		
		List<String> listLine = new ArrayList<String>();
		
		listLine.add(listLineInPath.get(0));
		
		for(int i = 0; i < x.length; i ++)
		{
			if(x[i])
				listLine.add(listLineInPath.get(i + 1));
		}
		
		String outPath = String.format("%s/%s.csv", outFolder, fileName);
		FileReaderWriter.writeFileByLine(outPath, listLine);
	}
	
//	/** @deprecated */
//	private String[] getFullPath(String inPathPre, String[] inPathPost)
//	{
//		int length = inPathPost.length;
//		String[] arrayPath = new String[length];
//		
//		for(int i = 0; i < length; i ++)
//			arrayPath[i] = inPathPre + inPathPost[i];
//		
//		return arrayPath;
//	}

}
