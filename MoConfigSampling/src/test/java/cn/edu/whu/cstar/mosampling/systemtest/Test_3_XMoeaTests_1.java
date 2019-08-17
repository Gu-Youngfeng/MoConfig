package cn.edu.whu.cstar.mosampling.systemtest;


import org.junit.Test;

import cn.edu.whu.cstar.experiments.ResultsDataCenter;
import cn.edu.whu.cstar.mosampling.moea.MOEA;
import cn.edu.whu.cstar.mosampling.moea.XMoeaProcessor;

public class Test_3_XMoeaTests_1 {

	
	String inPath = "testbed/input/rs-6d-c3-obj1_0.csv";
//	String inPath = "BerkeleyC.csv";
	
	String outFolder = "testbed/output";
	
	@Test
	public void test1()
	{
//		String base = "testbed/math_19";
//		String[] args = {
//			"1", "mutest.config", base + "/target/classes" + ":" + base + "/target/test-classes", base + "/src/test/java", "spooned_src", 
//			"new_test.log" 	
//		};
//		
//		App.main(args);
		
		XMoeaProcessor processor = new XMoeaProcessor();
//		processor.evaluateAll(1, 10000, inPath, outFolder, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.ENTROPY);
//		processor.evaluateAll(1, 10000, inPath, outFolder, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.VARIANCE);
		processor.evaluateAll(1, 10000, inPath, outFolder, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.DENSITY);

		ResultsDataCenter.printAllData();
//		processor.evaluateAll(10, 1000, "testbed/" + inPath, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.ENTROPY);
	}
	
}
