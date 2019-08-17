package cn.edu.whu.cstar.experiments;

import java.util.ArrayList;
import java.util.List;

import cn.edu.whu.cstar.mosampling.moea.MOEA.ObjectiveName;

/***
 * To save the experimental data using static functions, including addData() and getData().
 */
public class ResultsDataCenter {
	
	public static List<ResultsNode> listNodes = new ArrayList<>();
	
	ResultsDataCenter(){
		//Todo ...
	}
	
	public static void addData(ResultsNode node){
		listNodes.add(node);
	}
	
	public static List<List<Double>> getData(String projName, String methodName, ObjectiveName obj1, ObjectiveName obj2){
		if(listNodes.size() == 0) {
			return null;
		}
		
		List<List<Double>> data = null;
		for(int i=0; i<listNodes.size(); i++) {
			ResultsNode node = listNodes.get(i);
			if(node.projName.equals(projName) && node.methodName.equals(methodName) && node.obj1.equals(obj1) && node.obj2.equals(obj2)) {
				data = node.getResults();
				break;
			}
		}
		
		return data;
	}
	
	public static void printAllData() {
		if(listNodes.size() == 0) {
			return;
		}
		
		for(int i=0; i<listNodes.size(); i++) {
			ResultsNode node = listNodes.get(i);
			System.out.println(">> " + node.projName + " using [" + node.methodName + "] consdering " + node.obj1.toString() + " and " + node.obj2.toString()); 
			System.out.println(node.getResults().get(0));
			System.out.println(node.getResults().get(1));
			System.out.println();
		}
	}
		
	public static void clearAllData() {
		listNodes.clear();
	}

}
