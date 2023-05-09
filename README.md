Implementation of DSSE schemes. For now, the repo includes a Python implementation of the following schemes: Bestie [1], CLOSE-FB [2], FAST [3], Janus++ [4] and 
1. T. Chen, P. Xu, W. Wang, Y. Zheng, W. Susilo, and H. Jin, “Bestie: Very practical searchable encryption with forward and backward security,” in Computer Security – ESORICS 2021, E. Bertino, H. Shulman, and M. Waidner, Eds. Cham: Springer International Publishing, 2021, pp. 3–2
2.  K. He, J. Chen, Q. Zhou, R. Du, and Y. Xiang, “Secure dynamic searchable symmetric encryption with constant client storage cost,” IEEE Transactions on Information Forensics and Security, vol. 16, pp. 1538–1549, 202
3.  X. Song, C. Dong, D. Yuan, Q. Xu, and M. Zhao, “Forward private searchable symmetric encryption with optimized i/o efficiency,” IEEE Transactions on Dependable and Secure Computing, vol. 17, no. 5, pp. 912–927, 202
4.  S.-F. Sun, X. Yuan, J. K. Liu, R. Steinfeld, A. Sakzad, V. Vo, and S. Nepal, “Practical backward-secure searchable encryption from symmetric puncturable encryption,” in Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security, ser. CCS ’18. New York, NY, USA: Association for Computing Machinery, 2018, p. 763–7
5. Zhang H, Xu C, Lu R, et al. Non-interactive Multi-client Searchable Symmetric Encryption with Small Client Storage[J]. arXiv preprint arXiv:2212.02859, 2022.

Data set files with format. inverted_index_#####.txt contain the file identifiers of the Subject keyword.
data_owner.py demonstrates the data owner side.
data_user.py demonstrates the data user side.
server.py allows to search over the enrypted database.
data_owner_client.py is the update application file. It can be executed by command, python3 data_owner_client.py.
The parmater in data_owner_client.py can control the total number of files to be updated.

The main application demonstrates:

1.Setup with different data set
2.Encryption with time measurement
3.Deletion with time measurement
4.Search over the server.


**Usage**
python3 server.py
python3 data_owner.py
python3 data_owner_client.py
python3 data_user.py
