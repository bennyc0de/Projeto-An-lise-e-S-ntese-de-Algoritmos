#include <vector>
#include <unordered_map>
#include <cstdio>
#include <set>
#include <chrono> // Include the chrono library
#include <iostream> 

typedef struct
{
    std::set<int> stations;
    int num_stations;
} line;

std::vector<line> lines;

int N_stations;
int M_conects;
int L_lines;

int get_input()
{
    std::vector<bool> s_seen;
    int stationX, stationY, nline;
    if (scanf("%d %d %d", &N_stations, &M_conects, &L_lines) != 3)
    {
        return 1;
    }
    lines.resize(L_lines);
    s_seen.resize(N_stations);

    for (int c = 0; c < M_conects; c++)
    {
        if (scanf("%d %d %d", &stationX, &stationY, &nline) != 3)
        {
            return 1;
        }
        s_seen[stationX - 1] = true;
        s_seen[stationY - 1] = true;
        auto result1 = lines[nline - 1].stations.insert(stationX);
        if (result1.second)
        {
            lines[nline - 1].num_stations++;
        }
        auto result2 = lines[nline - 1].stations.insert(stationY);
        if (result2.second)
        {
            lines[nline - 1].num_stations++;
        }
    }
    for (auto e : s_seen)
    {
        if (!e)
        {
            return 1;
        }
    }

    return 0;
}

bool isSubset(std::set<int> &a, std::set<int> &b)
{
    for (int elem : a)
    {
        if (b.find(elem) == b.end())
        {
            return false;
        }
    }
    return true;
}

bool haveCommonElement(std::set<int> &a, std::set<int> &b)
{
    for (int elem : a)
    {
        if (b.find(elem) != b.end())
        {
            return true;
        }
    }
    return false;
}

void print_lines()
{
    for (int i = 0; i < L_lines; i++)
    {

        printf("Line %d (Stations: %d):", i, lines[i].num_stations);
        for (int station : lines[i].stations)
        {
            printf(" %d", station);
        }
        printf("\n");
    }
}

void sort_lines_by_size()
{
    for (size_t i = 0; i < lines.size(); ++i)
    {
        for (size_t j = 0; j < lines.size() - i - 1; ++j)
        {
            if (lines[j].num_stations > lines[j + 1].num_stations)
            {
                // Swap lines[j] and lines[j + 1]
                std::swap(lines[j], lines[j + 1]);
            }
        }
    }
}

std::vector<line> remove_useless_lines()
{
    std::vector<line> filtered;
    for (int i = 0; i < L_lines; ++i)
    {
        bool isSubsetOfAnother = false;
        for (int j = i + 1; j < L_lines; ++j)
        {
            if (isSubset(lines[i].stations, lines[j].stations))
            {
                isSubsetOfAnother = true;
                break;
            }
        }
        if (!isSubsetOfAnother)
        {
            filtered.push_back(lines[i]);
        }
    }

    return filtered;
}

void print_after_clean(std::vector<line> cleaned)
{
    for (const auto &s : cleaned)
    {
        printf("{ ");
        for (int x : s.stations)
        {
            printf("%d ", x);
        }
        printf(" } (size: %d )\n", s.num_stations);
    }
}

std::unordered_map<int, std::vector<int>> mount_graph(std::vector<line> cleaned)
{
    int len = cleaned.size();

    std::unordered_map<int, std::vector<int>> graph;

    for (int i = 0; i < len; ++i)
    {
        for (int j = i + 1; j < len; ++j)
        {
            if (haveCommonElement(cleaned[i].stations, cleaned[j].stations))
            {
                graph[i].push_back(j);
                graph[j].push_back(i);
            }
        }
    }
    return graph;
}

int bfs(int start, const std::unordered_map<int, std::vector<int>> &graph)
{
    std::unordered_map<int, int> distances;
    std::vector<int> q;

    for (const auto &node : graph)
    {
        distances[node.first] = -5;
    }

    distances[start] = 0;
    q.push_back(start);

    for (size_t i = 0; i < q.size(); ++i)
    {
        int current = q[i];

        for (int neighbor : graph.at(current))
        {
            if (distances[neighbor] == -5)
            {
                distances[neighbor] = distances[current] + 1;
                q.push_back(neighbor);
            }
        }
    }

    int max_cost = 0;
    for (const auto &entry : distances)
    {
        if (entry.second != -5)
        {
            if (entry.second > max_cost)
            {
                max_cost = entry.second;
            }
        }
    }

    return max_cost;
}

int main()
{
    auto start = std::chrono::high_resolution_clock::now();
    
    int highest_cost = 0;
    int temp;
    if (get_input())
    {
        printf("-1\n");
        return 0;
    }

    sort_lines_by_size();

    std::vector<line> cleaned = remove_useless_lines();

    std::unordered_map<int, std::vector<int>> graph = mount_graph(cleaned);

    if (cleaned.size() > 1 && graph.size() < cleaned.size())
    {
        printf("-1\n");

        auto end = std::chrono::high_resolution_clock::now(); // Record end time
        std::chrono::duration<double> duration = end - start; // Calculate duration

        std::cout << "Time taken: " << duration.count() << " seconds" << std::endl;

        return 0;
    }

    for (const auto &node : graph)
    {
        temp = bfs(node.first, graph);
        if (temp > highest_cost)
        {
            highest_cost = temp;
        }
    }

    printf("%d\n", highest_cost);

    auto end = std::chrono::high_resolution_clock::now(); // Record end time
    std::chrono::duration<double> duration = end - start; // Calculate duration

    std::cout << "Time taken: " << duration.count() << " seconds" << std::endl;

    return 0;
}