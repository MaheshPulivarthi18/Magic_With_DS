# Welcome to the Cash Flow Minimizer System README !!
#include <bits/stdc++.h>
using namespace std;

class bank{
    public:
    string name;
    int netAmount;
    set<string> types;
}; 

int getMinIndex(bank listOfNetAmounts[],int numBanks){
    int min=INT_MAX, minIndex=-1;
    for(int i=0;i<numBanks;i++){
        if(listOfNetAmounts[i].netAmount == 0) continue;
        
        if(listOfNetAmounts[i].netAmount < min){
            minIndex = i;
            min = listOfNetAmounts[i].netAmount;
        }
    }
    return minIndex;
}

int getSimpleMaxIndex(bank listOfNetAmounts[],int numBanks){
    int max=INT_MIN, maxIndex=-1;
    for(int i=0;i<numBanks;i++){
        if(listOfNetAmounts[i].netAmount == 0) continue;
        
        if(listOfNetAmounts[i].netAmount > max){
            maxIndex = i;
            max = listOfNetAmounts[i].netAmount;
        }
    }
    return maxIndex;
}

pair<int,string> getMaxIndex(bank listOfNetAmounts[],int numBanks,int minIndex,bank input[],int maxNumTypes){
    int max=INT_MIN;
    int maxIndex=-1;
    string matchingType;
    
    for(int i=0;i<numBanks;i++){
        if(listOfNetAmounts[i].netAmount == 0) continue;
        
        if(listOfNetAmounts[i].netAmount < 0) continue;
        
        //TODO 
        //see complexity of intersection
        
        vector<string> v(maxNumTypes);
        vector<string>::iterator ls=set_intersection(listOfNetAmounts[minIndex].types.begin(),listOfNetAmounts[minIndex].types.end(), listOfNetAmounts[i].types.begin(),listOfNetAmounts[i].types.end(), v.begin());
        
        if((ls-v.begin())!=0 && max<listOfNetAmounts[i].netAmount ){
            max=listOfNetAmounts[i].netAmount;
            maxIndex=i;
            matchingType = *(v.begin());
        } 
    }
    
    //if there is NO such max which has a common type with any remaining banks then maxIndex has -1
    // also return the common payment type
    return make_pair(maxIndex,matchingType);
}

void printAns(vector<vector<pair<int,string>>> ansGraph, int numBanks,bank input[]){
    
    cout<<"\nThe transactions for minimum cash flow are as follows : \n\n";
    for(int i=0;i<numBanks;i++){
        for(int j=0;j<numBanks;j++){
            
            if(i==j) continue;
            
            if(ansGraph[i][j].first != 0 && ansGraph[j][i].first != 0){
                
                if(ansGraph[i][j].first == ansGraph[j][i].first){
                    ansGraph[i][j].first=0;
                    ansGraph[j][i].first=0;
                }
                else if(ansGraph[i][j].first > ansGraph[j][i].first){
                    ansGraph[i][j].first -= ansGraph[j][i].first; 
                    ansGraph[j][i].first =0;
                    
                    cout<<input[i].name<<" pays Rs" << ansGraph[i][j].first<< "to "<<input[j].name<<" via "<<ansGraph[i][j].second<<endl;
                }
                else{
                    ansGraph[j][i].first -= ansGraph[i][j].first;
                    ansGraph[i][j].first = 0;
                    
                    cout<<input[j].name<<" pays Rs "<< ansGraph[j][i].first<<" to "<<input[i].name<<" via "<<ansGraph[j][i].second<<endl;
                    
                }
            }
            else if(ansGraph[i][j].first != 0){
                cout<<input[i].name<<" pays Rs "<<ansGraph[i][j].first<<" to "<<input[j].name<<" via "<<ansGraph[i][j].second<<endl;
                
            }
            else if(ansGraph[j][i].first != 0){
                cout<<input[j].name<<" pays Rs "<<ansGraph[j][i].first<<" to "<<input[i].name<<" via "<<ansGraph[j][i].second<<endl;
                
            }
            
            ansGraph[i][j].first = 0;
            ansGraph[j][i].first = 0;
        }
    }
    cout<<"\n";
}

void minimizeCashFlow(int numBanks,bank input[],unordered_map<string,int>& indexOf,int numTransactions,vector<vector<int>>& graph,int maxNumTypes){
    
    //Find net amount of each bank has
    bank listOfNetAmounts[numBanks];
    
    for(int b=0;b<numBanks;b++){
        listOfNetAmounts[b].name = input[b].name;
        listOfNetAmounts[b].types = input[b].types;
        
        int amount = 0;
        //incoming edges
        //column travers
        for(int i=0;i<numBanks;i++){
            amount += (graph[i][b]);
        }
        
        //outgoing edges
        //row traverse
        for(int j=0;j<numBanks;j++){
            amount += ((-1) * graph[b][j]);
        }
        
        listOfNetAmounts[b].netAmount = amount;
    }
    
    vector<vector<pair<int,string>>> ansGraph(numBanks,vector<pair<int,string>>(numBanks,{0,""}));//adjacency matrix
    
    
    //find min and max net amount
    int numZeroNetAmounts=0;
    
    for(int i=0;i<numBanks;i++){
        if(listOfNetAmounts[i].netAmount == 0) numZeroNetAmounts++;
    }
    while(numZeroNetAmounts!=numBanks){
        
        int minIndex=getMinIndex(listOfNetAmounts, numBanks);
        pair<int,string> maxAns = getMaxIndex(listOfNetAmounts, numBanks, minIndex,input,maxNumTypes);
        
        int maxIndex = maxAns.first;
        
        if(maxIndex == -1){
            
            (ansGraph[minIndex][0].first) += abs(listOfNetAmounts[minIndex].netAmount);
            (ansGraph[minIndex][0].second) = *(input[minIndex].types.begin());
            
            int simpleMaxIndex = getSimpleMaxIndex(listOfNetAmounts, numBanks);
            (ansGraph[0][simpleMaxIndex].first) += abs(listOfNetAmounts[minIndex].netAmount);
            (ansGraph[0][simpleMaxIndex].second) = *(input[simpleMaxIndex].types.begin());
            
            listOfNetAmounts[simpleMaxIndex].netAmount += listOfNetAmounts[minIndex].netAmount;
            listOfNetAmounts[minIndex].netAmount = 0;
            
            if(listOfNetAmounts[minIndex].netAmount == 0) numZeroNetAmounts++;
            
            if(listOfNetAmounts[simpleMaxIndex].netAmount == 0) numZeroNetAmounts++;
            
        }
        else{
            int transactionAmount = min(abs(listOfNetAmounts[minIndex].netAmount), listOfNetAmounts[maxIndex].netAmount);
            
            (ansGraph[minIndex][maxIndex].first) += (transactionAmount);
            (ansGraph[minIndex][maxIndex].second) = maxAns.second;
            
            listOfNetAmounts[minIndex].netAmount += transactionAmount;
            listOfNetAmounts[maxIndex].netAmount -= transactionAmount;
            
            if(listOfNetAmounts[minIndex].netAmount == 0) numZeroNetAmounts++;
            
            if(listOfNetAmounts[maxIndex].netAmount == 0) numZeroNetAmounts++;
        }
        
    }
    
    printAns(ansGraph,numBanks,input);
    // cout<<"HI\n";
}

//correct
int main() 
{ 
    cout<<"\n\t\t\t\t********************* Welcome to CASH FLOW MINIMIZER SYSTEM ***********************\n\n\n";
    cout<<"This system minimizes the number of transactions among multiple banks in the different corners of the world that use different modes of payment.There is one world bank (with all payment modes) to act as an intermediary between banks that have no common mode of payment. \n\n";
    cout<<"Enter the number of banks participating in the transactions.\n";
    int numBanks;cin>>numBanks;
    
    bank input[numBanks];
    unordered_map<string,int> indexOf;//stores index of a bank
    
    cout<<"Enter the details of the banks and transactions as stated:\n";
    cout<<"Bank name ,number of payment modes it has and the payment modes.\n";
    cout<<"Bank name and payment modes should not contain spaces\n";
    
    int maxNumTypes;
    for(int i=0; i<numBanks;i++){
        if(i==0){
            cout<<"World Bank : ";
        }
        else{
            cout<<"Bank "<<i<<" : ";
        }
        cin>>input[i].name;
        indexOf[input[i].name] = i;
        int numTypes;
        cin>>numTypes;
        
        if(i==0) maxNumTypes = numTypes;
        
        string type;
        while(numTypes--){
            cin>>type;
            
            input[i].types.insert(type);
        }   
        
    }
    
    cout<<"Enter number of transactions.\n";
    int numTransactions;
    cin>>numTransactions;
    
    vector<vector<int>> graph(numBanks,vector<int>(numBanks,0));//adjacency matrix
    
    cout<<"Enter the details of each transaction as stated:";
    cout<<"Debtor Bank , creditor Bank and amount\n";
    cout<<"The transactions can be in any order\n";
    for(int i=0;i<numTransactions;i++){
        cout<<(i)<<" th transaction : ";
        string s1,s2;
        int amount;
        cin >> s1>>s2>>amount;
        
        graph[indexOf[s1]][indexOf[s2]] = amount;
    }
     
    //settle
    minimizeCashFlow(numBanks,input,indexOf,numTransactions,graph,maxNumTypes);
    return 0; 
} 


/*
5
A 2 t1 t2
B 1 t1
C 1 t1
D 1 t2
E 1 t2
4
B A 300
C A 700
D B 500
E B 500

--------
5
World_Bank 2 Google_Pay PayTM
Bank_B 1 Google_Pay
Bank_C 1 Google_Pay
Bank_D 1 PayTM
Bank_E 1 PayTM
4
Bank_B World_Bank 300
Bank_C World_Bank 700
Bank_D Bank_B 500
Bank_E Bank_B 500

--------------------

6
B 3 1 2 3
C 2 1 2
D 1 2
E 2 1 3
F 1 3
G 2 2 3
9
G B 30
G D 10
F B 10
F C 30
F D 10
F E 10
B C 40
C D 20
D E 50
*/
This system minimizes the **number of transactions** among multiple banks in the different corners of the world that use **different modes of payment**. There is one world bank (with all payment modes) to act as an intermediary between banks that have no common mode of payment.

# Getting Started

Let's take an example. say we have the following banks:
1. Bank_of_America (World bank)
2. Wells_Fargo
3. Royal_Bank_of_Canada
4. Westpac
5. National_Australia_Bank
6. Goldman_Sachs

Following are the payments to be done:\
&emsp;&emsp;&emsp;    **Debtor Bank**&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;                **Creditor Bank** &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **Amount**
1. Goldman_Sachs   &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;             Bank_of_America &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;             Rs 100
2. Goldman_Sachs   &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;              Wells_Fargo &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;                Rs 300
3. Goldman_Sachs   &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;              Royal_Bank_of_Canada  &emsp;&emsp;&emsp;&emsp;&nbsp;      Rs 100
4. Goldman_Sachs   &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;              Westpac &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp; Rs 100
5. National_Australia_Bank &emsp;&emsp;&nbsp;&nbsp;       Bank_of_America &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp; Rs 300
6. National_Australia_Bank &emsp;&emsp;&nbsp;&nbsp;       Royal_Bank_of_Canada &emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Rs 100
7. Bank_of_America         &emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;       Wells_Fargo &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp; Rs 400
8. Wells_Fargo             &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;       Royal_Bank_of_Canada &emsp;&emsp;&emsp;&emsp;&nbsp; Rs 200
9. Royal_Bank_of_Canada    &emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp;      Westpac &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp; Rs 500


This is represented below as a directed graph with the directed edge representing debts.
![image](https://user-images.githubusercontent.com/54183085/110007387-9c625100-7d40-11eb-9128-29073ea4b3f3.png)

**But there's a catch!!**
Each Bank only supports a set of modes of payments and can _make_ or _receive_ payments **only** via those. Only World Bank suppports **all** modes of payments.
In our current example we have only three payment modes :
1. Google_Pay
2. AliPay
3. Paytm

Following is the list of Banks and their supported payment modes :
1. Bank_of_America &emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;- &emsp; Google_Pay, AliPay, Paytm
2. Wells_Fargo &emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&emsp;&nbsp;- &emsp; Google_Pay, AliPay
3. Royal_Bank_of_Canada &nbsp;&emsp;&nbsp;&nbsp;&nbsp;- &emsp; AliPay
4. Westpac &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;&nbsp; - &emsp; Google_Pay, Paytm
5. Goldman_Sachs &emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;- &emsp; Paytm
6. National_Australia_Bank &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - &emsp; AliPay, Paytm  

To pick the first Bank, we calculate the **net amount** for every Bank by using the below formula and store them in list:

net amount = [Sum of all **credits**(_amounts to be received_)] - [Sum of all **debits**(_amounts to pay_)]

Now the idea is that we are finding the bank which has _minimum_ net amount(_max debtor_) (_say Bank X, net amount x_) and then finding the bank which has the _maximum_ net amount( _max creditor_) (_say Bank Y, net amount y_) and also has a common payment mode (_say M1_) with the former bank. Then we find _minimum_ of absolute value of x and y, lets call it z.\
Now X pays the amount z to Y. Then 3 cases may arrived:
1. If (magnitude of x) < y  =>  X is completely settled and so removed from the list.
2. If (magnitude of x) > y  =>  Y is completely settled and so removed from the list.
3. If (magnitude of x) = y  =>  X and Y both are completely settled and so both are removed from the list.

The same process is repeated for the remaining banks.\
For the current example, the transactions for minimum cash flow are as follows:

![image](https://user-images.githubusercontent.com/54183085/110007435-aab06d00-7d40-11eb-8e0c-ea5c7ec762a3.png)

So this is the required answer.

# How to Use?
This system is completely **menu-driven**. So when you will run the C++ Application, it will guide you and show you the final output.\
Below is the execution of our current example:
![image](https://user-images.githubusercontent.com/54183085/110011598-a33f9280-7d45-11eb-9499-a2868924cefd.png)

Thank you!!
Happy learning :)
