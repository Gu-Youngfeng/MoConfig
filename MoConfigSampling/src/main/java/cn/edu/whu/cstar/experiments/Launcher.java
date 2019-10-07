package cn.edu.whu.cstar.experiments;

import java.io.File;

import cn.edu.whu.cstar.mosampling.moea.MoConfigProblem;
import cn.edu.whu.cstar.mosampling.moea.XMoeaProcessor;

/**
 * <p>Class Launcher is the main entry of the MoConfigSampling project.</p>
 * @author yongfeng
 * @update 2019.10.5
 */
public class Launcher {
	/** folder to save the input projects*/
	public static final String INPUT_FOLDER = "testbed/input/";
	/** folder to save the output experimental results*/
	public static final String OUTPUT_FOLDER = "testbed/output/";
	/** experimental repeat time*/
	public static int EXP_ROUNDS = 1;
	/** default pair is "variance-cost", this can be changed by 0,1,2,3,... */
	public static int COMBINE_TYPE = 3;
	/** stop criteria of MOEA algorithm*/
	public static int MAX_EVALUATION_NUM = 10000;
	
	public static void main(String[] args){	
		new Launcher().runExp();		
	}
	
	public void runExp() {
		
		File[] lsProjs = new File(INPUT_FOLDER).listFiles(); // lsFiles: all 21 projects in the input folder
		int projsSize = lsProjs.length; // 21
		
		String[] projPaths = new String[projsSize];
		for(int i=0; i<projsSize; i++) {
			projPaths[i] = INPUT_FOLDER + lsProjs[i].getName(); // inPaths[i]: the relative path of the i-th project in the input folder
		}
		
		long[][] times = new long[EXP_ROUNDS][projsSize];
		
		for(int round=0; round<EXP_ROUNDS;round++) {
			long[] timeCost = new long[projsSize]; // time cost of each project in one round
			
			for(int k=0; k<projsSize; k++) {
				String inPath = projPaths[k];	// project path
				String projName = lsProjs[k].getName(); // project name
				System.out.println("### " + projName + "\n");
				
				long startTime = System.currentTimeMillis(); // start time
				
				runMoConfig(COMBINE_TYPE, inPath);
				
				long endTime = System.currentTimeMillis(); // end time
								
				timeCost[k] = endTime - startTime;
				ResultsDataCenter.printAllData();  // print the solutions with objective values
				ResultsDataCenter.clearAllData();
			}
			times[round] = timeCost;
			
		}
		
		// print the time cost
		System.out.println("Time cost of each proiject:");
		for(int j=0; j<projsSize; j++) {  // for each csv file
			int sum = 0;
			for(int i=0; i<EXP_ROUNDS; i++) { // sum of all rounds
				sum += times[i][j];
			}
			System.out.print(sum*1.0/EXP_ROUNDS + ","); // average time cost
		}
	}
	
	/** To run MoConfig with combineType
	 * @param combineType combine type: 0, 1, 2, 3
	 * */
	public void runMoConfig(int combineType, String inPath) {
		XMoeaProcessor processor = new XMoeaProcessor();
		
		switch(combineType) {
		case 0: // try entropy-cost pair
			processor.evaluateAll(1, MAX_EVALUATION_NUM, inPath, OUTPUT_FOLDER, MoConfigProblem.ObjectiveName.NUMSAMPLE, MoConfigProblem.ObjectiveName.ENTROPY);
			break;
		case 1: // try variance-cost pair
			processor.evaluateAll(1, MAX_EVALUATION_NUM, inPath, OUTPUT_FOLDER, MoConfigProblem.ObjectiveName.NUMSAMPLE, MoConfigProblem.ObjectiveName.VARIANCE);
			break;
		case 2: // try density-cost pair
			processor.evaluateAll(1, MAX_EVALUATION_NUM, inPath, OUTPUT_FOLDER, MoConfigProblem.ObjectiveName.NUMSAMPLE, MoConfigProblem.ObjectiveName.DENSITY);
			break;
		default: // try all objective pairs 
			processor.evaluateAll(1, MAX_EVALUATION_NUM, inPath, OUTPUT_FOLDER, MoConfigProblem.ObjectiveName.NUMSAMPLE, MoConfigProblem.ObjectiveName.ENTROPY);
			processor.evaluateAll(1, MAX_EVALUATION_NUM, inPath, OUTPUT_FOLDER, MoConfigProblem.ObjectiveName.NUMSAMPLE, MoConfigProblem.ObjectiveName.VARIANCE);
			processor.evaluateAll(1, MAX_EVALUATION_NUM, inPath, OUTPUT_FOLDER, MoConfigProblem.ObjectiveName.NUMSAMPLE, MoConfigProblem.ObjectiveName.DENSITY);
			break;
		}
	}
		
}