#include <bits/stdc++.h>
using namespace std;

class bank
{
public:
    string name;
    int netAmount;
    set<string> types;
};

int getMinIndex(bank listOfNetAmounts[], int numBanks)
{
    int min = INT_MAX, minIndex = -1;
    for (int i = 0; i < numBanks; i++)
    {
        if (listOfNetAmounts[i].netAmount == 0)
            continue;

        if (listOfNetAmounts[i].netAmount < min)
        {
            minIndex = i;
            min = listOfNetAmounts[i].netAmount;
        }
    }
    return minIndex;
}

int getSimpleMaxIndex(bank listOfNetAmounts[], int numBanks)
{
    int max = INT_MIN, maxIndex = -1;
    for (int i = 0; i < numBanks; i++)
    {
        if (listOfNetAmounts[i].netAmount == 0)
            continue;

        if (listOfNetAmounts[i].netAmount > max)
        {
            maxIndex = i;
            max = listOfNetAmounts[i].netAmount;
        }
    }
    return maxIndex;
}

pair<int, string> getMaxIndex(bank listOfNetAmounts[], int numBanks, int minIndex, bank input[] __attribute__((unused)), int maxNumTypes)
{
    int max = INT_MIN;
    int maxIndex = -1;
    string matchingType;

    for (int i = 0; i < numBanks; i++)
    {
        if (listOfNetAmounts[i].netAmount == 0)
            continue;

        if (listOfNetAmounts[i].netAmount < 0)
            continue;

        vector<string> v(maxNumTypes);
        vector<string>::iterator ls = set_intersection(
            listOfNetAmounts[minIndex].types.begin(), listOfNetAmounts[minIndex].types.end(),
            listOfNetAmounts[i].types.begin(), listOfNetAmounts[i].types.end(), v.begin());

        if ((ls - v.begin()) != 0 && max < listOfNetAmounts[i].netAmount)
        {
            max = listOfNetAmounts[i].netAmount;
            maxIndex = i;
            matchingType = *(v.begin());
        }
    }

    return make_pair(maxIndex, matchingType);
}

void printAns(vector<vector<pair<int, string>>> ansGraph, int numBanks, bank input[])
{
    cout << "\nThe transactions for minimum cash flow are as follows : \n\n";
    for (int i = 0; i < numBanks; i++)
    {
        for (int j = 0; j < numBanks; j++)
        {
            if (i == j)
                continue;

            if (ansGraph[i][j].first != 0 && ansGraph[j][i].first != 0)
            {
                if (ansGraph[i][j].first == ansGraph[j][i].first)
                {
                    ansGraph[i][j].first = 0;
                    ansGraph[j][i].first = 0;
                }
                else if (ansGraph[i][j].first > ansGraph[j][i].first)
                {
                    ansGraph[i][j].first -= ansGraph[j][i].first;
                    ansGraph[j][i].first = 0;
                    cout << input[i].name << " pays Rs " << ansGraph[i][j].first << " to " << input[j].name << " via " << ansGraph[i][j].second << endl;
                }
                else
                {
                    ansGraph[j][i].first -= ansGraph[i][j].first;
                    ansGraph[i][j].first = 0;
                    cout << input[j].name << " pays Rs " << ansGraph[j][i].first << " to " << input[i].name << " via " << ansGraph[j][i].second << endl;
                }
            }
            else if (ansGraph[i][j].first != 0)
            {
                cout << input[i].name << " pays Rs " << ansGraph[i][j].first << " to " << input[j].name << " via " << ansGraph[i][j].second << endl;
            }
            else if (ansGraph[j][i].first != 0)
            {
                cout << input[j].name << " pays Rs " << ansGraph[j][i].first << " to " << input[i].name << " via " << ansGraph[j][i].second << endl;
            }

            ansGraph[i][j].first = 0;
            ansGraph[j][i].first = 0;
        }
    }
    cout << "\n";
}

void minimizeCashFlow(int numBanks, bank input[] __attribute__((unused)), unordered_map<string, int> &indexOf __attribute__((unused)), int numTransactions __attribute__((unused)), vector<vector<int>> &graph, int maxNumTypes)
{
    bank listOfNetAmounts[numBanks];

    for (int b = 0; b < numBanks; b++)
    {
        listOfNetAmounts[b].name = input[b].name;
        listOfNetAmounts[b].types = input[b].types;

        int amount = 0;

        for (int i = 0; i < numBanks; i++)
        {
            amount += (graph[i][b]);
        }

        for (int j = 0; j < numBanks; j++)
        {
            amount += ((-1) * graph[b][j]);
        }

        listOfNetAmounts[b].netAmount = amount;
    }

    vector<vector<pair<int, string>>> ansGraph(numBanks, vector<pair<int, string>>(numBanks, {0, ""}));

    int numZeroNetAmounts = 0;

    for (int i = 0; i < numBanks; i++)
    {
        if (listOfNetAmounts[i].netAmount == 0)
            numZeroNetAmounts++;
    }
    while (numZeroNetAmounts != numBanks)
    {
        int minIndex = getMinIndex(listOfNetAmounts, numBanks);
        pair<int, string> maxAns = getMaxIndex(listOfNetAmounts, numBanks, minIndex, input, maxNumTypes);

        int maxIndex = maxAns.first;

        if (maxIndex == -1)
        {
            (ansGraph[minIndex][0].first) += abs(listOfNetAmounts[minIndex].netAmount);
            (ansGraph[minIndex][0].second) = *(input[minIndex].types.begin());

            int simpleMaxIndex = getSimpleMaxIndex(listOfNetAmounts, numBanks);
            (ansGraph[0][simpleMaxIndex].first) += abs(listOfNetAmounts[minIndex].netAmount);
            (ansGraph[0][simpleMaxIndex].second) = *(input[simpleMaxIndex].types.begin());

            listOfNetAmounts[simpleMaxIndex].netAmount += listOfNetAmounts[minIndex].netAmount;
            listOfNetAmounts[minIndex].netAmount = 0;

            if (listOfNetAmounts[minIndex].netAmount == 0)
                numZeroNetAmounts++;

            if (listOfNetAmounts[simpleMaxIndex].netAmount == 0)
                numZeroNetAmounts++;
        }
        else
        {
            int transactionAmount = min(abs(listOfNetAmounts[minIndex].netAmount), listOfNetAmounts[maxIndex].netAmount);

            (ansGraph[minIndex][maxIndex].first) += (transactionAmount);
            (ansGraph[minIndex][maxIndex].second) = maxAns.second;

            listOfNetAmounts[minIndex].netAmount += transactionAmount;
            listOfNetAmounts[maxIndex].netAmount -= transactionAmount;

            if (listOfNetAmounts[minIndex].netAmount == 0)
                numZeroNetAmounts++;

            if (listOfNetAmounts[maxIndex].netAmount == 0)
                numZeroNetAmounts++;
        }
    }

    printAns(ansGraph, numBanks, input);
}

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        cerr << "Usage: " << argv[0] << " <banks_file> <transactions_file>" << endl;
        return 1;
    }

    ifstream banks_file(argv[1]);
    ifstream transactions_file(argv[2]);

    if (!banks_file.is_open() || !transactions_file.is_open())
    {
        cerr << "Error opening file(s)." << endl;
        return 1;
    }

    int numBanks;
    banks_file >> numBanks;

    bank input[numBanks];
    unordered_map<string, int> indexOf;
    int maxNumTypes = 0;

    for (int i = 0; i < numBanks; i++)
    {
        banks_file >> input[i].name;
        indexOf[input[i].name] = i;
        int numTypes;
        banks_file >> numTypes;

        if (numTypes > maxNumTypes)
        {
            maxNumTypes = numTypes;
        }

        string type;
        for (int j = 0; j < numTypes; j++)
        {
            banks_file >> type;
            input[i].types.insert(type);
        }
    }

    int numTransactions;
    transactions_file >> numTransactions;

    vector<vector<int>> graph(numBanks, vector<int>(numBanks, 0));

    for (int i = 0; i < numTransactions; i++)
    {
        string s1, s2;
        int amount;
        transactions_file >> s1 >> s2 >> amount;

        graph[indexOf[s1]][indexOf[s2]] = amount;
    }

    minimizeCashFlow(numBanks, input, indexOf, numTransactions, graph, maxNumTypes);

    // Close the files
    banks_file.close();
    transactions_file.close();

    return 0;
}
