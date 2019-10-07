package cn.edu.whu.cstar.mosampling.moea;

import java.util.List;

import cn.edu.whu.cstar.mosampling.tool.FileReaderWriter;

/***
 * <p>Class InstanceReader reads instance from .csv file and then constructs the results in a 2-dimensional way.
 * Call the variable {@link#matrixValue} to get the results. 
 * </p>
 * @author jifeng
 * @update 2019.10.5
 */
public class InstanceReader {

	/** instances, where i is the configuration index and j is the option index*/
	double[][] matrixValue = null; // save all the configuration into the 2-dimension array, matrixValue
		
	int numOption = 8; // default number of options, this must be re-assigned in readInstance()
	int numConfiguration = -1; // default number of configurations, this must be re-assigned in readInstance()
	
	public InstanceReader(String inPath) {
		readInstance(inPath);
	}
	
	/** To get instance from the csv file in path. 
	 *  The 1-st line in the csv file describes the options while the others shows the instance data.
	 * */
	public void readInstance(String inPath){
		
		List<String> listLine = FileReaderWriter.readFileByLine(inPath);
		numConfiguration = listLine.size() -1; 
		
		String line = null;
		double value = -1;
		
		line = listLine.get(0); // the 1st line in .csv file presents the option name and performance name
		String[] arrayToken = line.split(",");
		numOption = arrayToken.length -1; // assignment of numOption
		
		matrixValue = new double[numConfiguration][numOption]; // save all the configuration into the 2-dimension array, matrixValue
		
		for(int i = 1; i < numConfiguration; i ++)
		{
			line = listLine.get(i);
			arrayToken = line.split(",");
			
			for(int j = 0; j < numOption; j ++)
			{
				String token = arrayToken[j];
				value = Double.parseDouble(token);
				matrixValue[i][j] = value;
			}
		}	
	}
}