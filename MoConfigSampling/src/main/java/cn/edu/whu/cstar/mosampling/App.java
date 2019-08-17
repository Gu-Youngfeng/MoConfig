package cn.edu.whu.cstar.mosampling;

import java.io.File;

import cn.edu.whu.cstar.experiments.ResultsDataCenter;
import cn.edu.whu.cstar.mosampling.moea.MOEA;
import cn.edu.whu.cstar.mosampling.moea.XMoeaProcessor;

/**
 * <p>Class App is the main entry of the MoConfigSampling project.</p>
 */
public class App {

//	public static void main(String[] args) 
//	{
//		long startTime = System.currentTimeMillis(); // start time
//
//		if(args.length < 3) // in case of lack of parameters
//		{
//			printUsage();
//			return;
//		}
//		
//		int paramIndex = 0; 
//		
//		String strIndex = args[paramIndex ++];
//		
//		switch(strIndex)
//		{
//		case "3":	
//		case "--execution":
//		// TODO
//			
////			System.out.println("Operation: " + "--execution");
////			
////			if(args.length - paramIndex != 6)
////				printUsage();
////			else
////			{
////				XMoeaProcessor processor = new XMoeaProcessor();
////				processor.evaluateAll(1, 10000, "testbed/input/" + inPath, outFolder, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.ENTROPY);
////			}
////			
//			break;	
//		default:	
//			printUsage();			
//		}
//		
//		long endTime = System.currentTimeMillis();
//		endTime = (endTime - startTime)/1000;
//		
//		System.out.println();
//		System.out.println(String.format("Time cost:\t%d min\t%d sec.", endTime /60, endTime %60));
//	}
//
//	private static void printUsage()
//	{
//		System.out.println("Usage: ");
//		System.out.println(TAB + "java -jar mutest.jar --mutation|--compilation|--execution ...");
//	}
	
//	private final static String TAB = "\t";
	
	public static void main(String[] args){
		String inputFolder = "testbed/input/";
		String outFolder = "testbed/output/";
		
		File[] lsFiles = new File(inputFolder).listFiles(); // all files in $inputFolder
		int fileSize = lsFiles.length;
		
		String[] inPaths = new String[fileSize];
		for(int i=0; i<fileSize; i++) inPaths[i] = inputFolder + lsFiles[i].getName(); // all file names in $inputFolder
		int rounds = 1;
		long[][] times = new long[rounds][fileSize];
		
		for(int round=0; round<rounds;round++) {
			long[] timeCost = new long[fileSize];
			
			for(int k=0; k<fileSize; k++) {
				String inPath = inPaths[k];	// input project
		//		System.out.println(inPath);
				String projName = lsFiles[k].getName(); // project name
//				System.out.println("### " + projName + "\n");
				
				long startTime = System.currentTimeMillis(); // start time
				
				int combineType = 1; // default pair is "variance-cost", this can be changed by 0,1,2,3,... 
				
				XMoeaProcessor processor = new XMoeaProcessor();
				
				switch(combineType){
				case 0: // try entropy-cost pair
					processor.evaluateAll(1, 10000, inPath, outFolder, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.ENTROPY);
					break;
				case 1: // try variance-cost pair
					processor.evaluateAll(1, 10000, inPath, outFolder, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.VARIANCE);
					break;
				case 2: // try density-cost pair
					processor.evaluateAll(1, 10000, inPath, outFolder, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.DENSITY);
					break;
				default: // try all objective pairs 
					processor.evaluateAll(1, 10000, inPath, outFolder, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.ENTROPY);
					processor.evaluateAll(1, 10000, inPath, outFolder, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.VARIANCE);
					processor.evaluateAll(1, 10000, inPath, outFolder, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.DENSITY);
					break;
				}
				
				long endTime = System.currentTimeMillis(); // end time
				
				
				timeCost[k] = endTime - startTime;
				ResultsDataCenter.printAllData();  // print the solutions with objective values
				ResultsDataCenter.clearAllData();
			}
			times[round] = timeCost;
			
		}
		
		// print the time cost
		for(int j=0; j<fileSize; j++) {
			int sum = 0;
			for(int i=0; i<rounds; i++) {
				sum += times[i][j];
			}
			System.out.print(sum*1.0/rounds + ",");
		}
		
	}
	
	
}