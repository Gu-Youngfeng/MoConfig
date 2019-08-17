package cn.edu.whu.cstar.experiments;

import java.util.ArrayList;
import java.util.List;

import cn.edu.whu.cstar.mosampling.moea.MOEA.ObjectiveName;

public class ResultsNode {
	
	public String projName = "";
	public String methodName = "";
	
	public ObjectiveName obj1;
	public ObjectiveName obj2;
	
	private List<List<Double>> data;
	
	public ResultsNode(String projName, String methodName, ObjectiveName obj1, ObjectiveName obj2) {
		this.projName = projName;
		this.methodName = methodName;
		this.obj1 = obj1;
		this.obj2 = obj2;
	}
	
	public void saveResults(List<Double> obj1, List<Double> obj2) {
		List<Double> ListObj1 = new ArrayList<Double> (obj1);
		List<Double> ListObj2 = new ArrayList<Double> (obj2);
		data = new ArrayList<>();
		data.add(ListObj1);
		data.add(ListObj2);
	}
	
	public List<List<Double>> getResults(){
		return data;
	}

}
