import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import com.github.javaparser.JavaParser;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.body.BodyDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.CastExpr;
import com.github.javaparser.ast.expr.Expression;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.stmt.BlockStmt;
import com.github.javaparser.ast.stmt.ExpressionStmt;
import com.github.javaparser.ast.visitor.ModifierVisitor;

public class AddAsserts extends ModifierVisitor {
	static boolean flag=false;
	@SuppressWarnings("unchecked")
	static File test_temp=null;
	static ArrayList<ArrayList<String>> testvalues=new ArrayList<ArrayList<String>>();//contains list of args to pass to assertions
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		//takes arg0 as path test template file to parse exists, arg1: filepath to test cases to add to assertion in format ;#; separated args and each test per line
    	//args[0]="D:/Desktop/Crosslib_python/CrossLibTest/query/test_temp.java";
    	test_temp = new File(args[0]);
    	ArrayList<String> testcases_linewise=(ArrayList<String>) Files.readAllLines(Paths.get(args[1]),StandardCharsets.ISO_8859_1);
    	/**
         * Read val from file and pass as is
         * extract method name for assertion stmt prep
         * 
         */
    	for(String line:testcases_linewise)
    	{ArrayList<String> vals=new ArrayList<String>();
    		String[] argvals=line.split(";#;");
    		for(int i=0;i<argvals.length;i++)
    		{
    			vals.add(argvals[i]);
    		}
    		testvalues.add(vals);
    	}
    	 CompilationUnit classcode = StaticJavaParser.parse(test_temp,StandardCharsets.ISO_8859_1);
         AddAsserts visitor=new AddAsserts();
         visitor.visit(classcode, null);
       }
    
    @Override
    public Node visit(ExpressionStmt call, Object arg) {
    	super.visit(call, arg);
    	//System.out.println(call.getExpression().toString());
       BlockStmt block=null;
    	if(!flag)
        {//System.out.println(call.getExpression().toString());
    		String call_prefix=(call.getExpression().toString().split(",")[1]).trim().split("\\(")[0];
        	block=(BlockStmt) call.getParentNode().get();
        	//block.addStatement("System.out.println(\"testing\");");
        	for(ArrayList<String> vals: testvalues)
        	{
        		String exp_op=vals.get(0);
        		String args="";//as comma separated values
        		for(int i=1;i<vals.size();i++)
        		{
        			args=args+vals.get(i)+",";
        		}
        		args=args.substring(0,args.length()-1);//remove last comma
        		String stmt="assertEquals("+exp_op+","+call_prefix+"("+args+"));";
        		//System.out.println(stmt);
        		try{
        		block.addStatement(stmt);//frame stmt and pass args in loop
        		}catch(com.github.javaparser.ParseProblemException e){continue;}
        	}
        	CompilationUnit cu=block.findCompilationUnit().get();
        	//System.out.println(cu);
        	//write modified compilation unit to a file
            try {
				Files.write(test_temp.toPath(), cu.toString().getBytes());
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
            
        	flag=true;
        }
		return block;
       }

	
   	
	/*private static class ReturnStmtChangerVisitor extends ModifierVisitor<Void> {
		@Override
		public Node visit(ReturnStmt returnStmt, Void arg) {
			BlockStmt parentBlock = (BlockStmt) returnStmt.getParentNode().get();
			int indexInParent = parentBlock.getChildNodes().indexOf(returnStmt);
			MethodDeclaration method = returnStmt.getAncestorOfType(MethodDeclaration.class).get();
			if(method.getType() instanceof VoidType) {
				parentBlock.addStatement(indexInParent, JavaParser.parseStatement("logger.debug(\"methodReturnValue:void\");"));
			}
			else {
				parentBlock.addStatement(indexInParent, JavaParser.parseStatement(method.getType().toString() + " methodReturnValue = " + returnStmt.getExpression().get() + ";"));
				returnStmt.setExpression(JavaParser.parseExpression("methodReturnValue"));
			}
			return returnStmt;
		}
	}*/
}
