package cn.edu.whu.cstar.mosampling.systemtest;


import org.junit.Test;

import cn.edu.whu.cstar.mosampling.moea.MOEA;
import cn.edu.whu.cstar.mosampling.moea.XMoeaProcessor;

public class Test_3_XMoeaTests_2 {

	
//	String inPath = "wc+rs-3d-c4-obj1.csv";
	String inPath = "BerkeleyC.csv";
	
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
		processor.evaluateAll(1, 10000, "testbed/input/" + inPath, outFolder, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.ENTROPY);
//		processor.evaluateAll(1, 10000, "testbed/input/" + inPath, outFolder, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.VARIANCE);
//		processor.evaluateAll(1, 10000, "testbed/input/" + inPath, outFolder, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.DENSITY);

		
//		processor.evaluateAll(10, 1000, "testbed/" + inPath, MOEA.ObjectiveName.NUMSAMPLE, MOEA.ObjectiveName.ENTROPY);
	}
	
}
